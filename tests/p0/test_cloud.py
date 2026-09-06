import sys
from pathlib import Path
import unittest
from unittest.mock import patch
from datetime import timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/p0'))
from cloud import timeline

class TimelineTests(unittest.TestCase):
    def test_only_distinct_scheduled_mornings_count(self):
        def sample(day,event='schedule'):
            return {'observed_at':f'2026-09-{day:02d}T09:10:00+00:00','event':event,'results':[]}
        with patch('cloud.ZoneInfo',return_value=timezone.utc):
            md=timeline([sample(6),sample(6),sample(7,'workflow_dispatch'),sample(8)])
        self.assertIn('distintas observadas por agendamento (09h–12h): 2',md)
        self.assertIn('insuficiente',md)
    def test_failure_does_not_overwrite_previous_valid_hashes(self):
        def sample(day,status,ids):
            return {'observed_at':f'2026-09-{day:02d}T09:10:00+00:00','event':'schedule',
                    'results':[{'id':'test','status':status,'item_count':len(ids),
                                'items':[{'id_hash':x} for x in ids]}]}
        with patch('cloud.ZoneInfo',return_value=timezone.utc):
            md=timeline([sample(6,'ok',['a']),sample(7,'http_error',[]),sample(8,'ok',['a','b'])])
        self.assertIn('| test | ok | 2 | 1 |',md)
        self.assertIn('não concede direitos',md)

if __name__=='__main__': unittest.main()
