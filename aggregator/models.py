from minimongo import Model, Index
from hashlib import md5
import time
from logger import Logger

class RunRecord(Model):
    class Meta:
        database = 'ml_dashboard'
        collection = 'aggregator_runrecord'
        indices = ( Index('key'), )

    @classmethod
    def GenerateUniqueKey(cls, actions, data_point):
        unique_key = data_point['type']
        if 'sub_type' in data_point:
            unique_key += data_point['sub_type']
        if 'elements' in data_point:
            unique_key += ''.join([e['value'] for e in data_point['elements']])
        if actions:
            unique_key += ''.join([a['name'] for a in actions])
        return md5(unique_key).hexdigest()

    @classmethod
    def LastSuccess(cls, data_point, actions=None):
        Logger.Info('%s - RunRecord.LastSuccess - started' % __name__)
        Logger.Debug('%s - RunRecord.LastSuccess - started with data_point:%s and actions:%s' % (__name__, data_point, actions))
        key = cls.GenerateUniqueKey(actions, data_point)
        run_record = RunRecord.collection.find_one({'key':key})
        if not run_record:
            return None
        last_success = run_record['last_success']
        Logger.Info('%s - RunRecord.LastSuccess - started' % __name__)
        return last_success

    @classmethod
    def RecordRun(cls, data_point, actions=None):
        Logger.Info('%s - RunRecord.RecordRun - started' % __name__)
        Logger.Debug('%s - RunRecord.RecordRun - started with data_point:%s and actions:%s' % (__name__, data_point, actions))
        key = cls.GenerateUniqueKey(actions, data_point)
        run_record = RunRecord.collection.find_one({'key':key})
        if not run_record:
            run_record = RunRecord({'key':key})
        run_record['last_success'] = time.time()
        run_record.save()
        Logger.Info('%s - RunRecord.RecordRun - finished' % __name__)