from controllers import AggregationController
from logger import Logger
from utils import  JSONResponse

#@async
def run_all_dashboards(request):
    Logger.Info('%s - run_all_dashboards - started' % __name__)
    aggregator = AggregationController()
    aggregator.aggregate()
    Logger.Info('%s - run_all_dashboards - finished' % __name__)
    return JSONResponse({'status':'success'})

