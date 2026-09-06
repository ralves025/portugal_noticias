import sys
from pathlib import Path
import unittest
from datetime import datetime, timezone
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'scripts/p0'))
from probe import canonical, parse_feed, validate_target, probe
NOW=datetime(2026,9,6,8,tzinfo=timezone.utc)

class ProbeTests(unittest.TestCase):
    def test_rss_duplicate_dates_and_no_article_text(self):
        xml=b'<rss><channel><item><title>FICTICIO</title><link>/a?utm_source=x&amp;id=1</link><pubDate>Sun, 06 Sep 2026 07:00:00 GMT</pubDate></item><item><title>FICTICIO</title><link>/a?id=1</link></item></channel></rss>'
        report, urls=parse_feed(xml,'https://example.com/feed',NOW)
        self.assertEqual(report['item_count'],2)
        self.assertEqual(report['duplicate_urls'],1)
        self.assertEqual(report['missing_dates'],1)
        self.assertNotIn('FICTICIO',str(report))
        self.assertEqual(urls,['https://example.com/a?id=1'])
    def test_atom_and_future_date(self):
        xml=b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>FICTICIO</title><link href="/b"/><published>2026-09-07T08:00:00Z</published><category term="Cultura"/></entry></feed>'
        report, urls=parse_feed(xml,'https://example.com/',NOW)
        self.assertEqual(report['future_dates'],1)
        self.assertIsNone(report['items'][0]['published_at'])
        self.assertEqual(report['categories'],{'Cultura':1})
    def test_missing_and_invalid_fields(self):
        r,_=parse_feed(b'<rss><channel><item><link>javascript:alert(1)</link><pubDate>bad</pubDate></item></channel></rss>','https://example.com',NOW)
        self.assertEqual((r['missing_titles'],r['invalid_links'],r['invalid_dates']),(1,1,1))
    def test_reject_malicious_xml_and_html(self):
        for xml in (b'<!DOCTYPE rss [<!ENTITY x "bad">]><rss/>',b'<html/>',b'<rss>', '<rss/>'.encode('utf-16')):
            with self.subTest(xml=xml), self.assertRaises((ValueError,UnicodeError)):
                # XML ParseError is a SyntaxError, covered separately below.
                try: parse_feed(xml,'https://example.com',NOW)
                except SyntaxError as e: raise ValueError('malformed') from e
    def test_canonical_preserves_functional_query(self):
        self.assertEqual(canonical('/a/?page=2&utm_source=x#part','https://example.com'), 'https://example.com/a/?page=2')
    def test_private_or_unlisted_targets_rejected(self):
        with self.assertRaises(ValueError): validate_target('https://evil.example', ['example.com'])
        with patch('probe.socket.getaddrinfo',return_value=[(0,0,0,'',('127.0.0.1',443))]):
            with self.assertRaises(ValueError): validate_target('https://example.com',['example.com'])
    def test_http_failure_becomes_finding(self):
        e={'id':'test','url':'https://example.com','hosts':['example.com']}
        with patch('probe.fetch',return_value=(b'',{'http_status':429,'retry_after':'60'})):
            r=probe(e,NOW)
        self.assertEqual(r['status'],'http_error')
        self.assertFalse(r['publication_approved'])

if __name__=='__main__': unittest.main()
