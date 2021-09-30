import time
import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine

logger = logging.getLogger("app.sqltime")

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    print("Hello")
    context._query_start_time = time.time()
    logger.debug("Query: %s", statement)
    logger.debug("Parameters:\n%r" % parameters)

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    print("Hello")
    total = time.time() - context._query_start_time
    logger.debug("Query Complete!")
    logger.debug("Total Time: %.02fms" % (total*1000))