from typing import List

from metric_type import MetricGaugeType
from prometheus_client import start_http_server, Gauge


class MetricsHelper:
    _metrics = None

    def __init__(self, bot) -> None:
        self.__bot = bot
        self.__start_metrics_server()

    def __start_metrics_server(self):
        if not self.__bot.bot_config.EXPOSE_METRICS or self._metrics is not None:
            return
        start_http_server(3142)
        self.__bot.log.info("Prometheus Metrics endpoint is available on port 3142")
        self._metrics = {
            MetricGaugeType.TOTAL_RECEIVED_MESSAGES: Gauge("accessbot_total_received_messages", "total count of received messages"),
            MetricGaugeType.TOTAL_ACCESS_REQUESTS: Gauge("accessbot_total_access_requests", "total count of received access requests messages"),
            MetricGaugeType.TOTAL_MANUAL_APPROVALS: Gauge("accessbot_total_manual_approvals", "total count of manually approved access requests"),
            MetricGaugeType.TOTAL_AUTO_APPROVALS: Gauge("accessbot_total_auto_approvals", "total count of auto approved access requests"),
            MetricGaugeType.TOTAL_MANUAL_DENIALS: Gauge("accessbot_total_denied_access_requests", "total count of denied access requests"),
            MetricGaugeType.TOTAL_TIMED_OUT_REQUESTS: Gauge("accessbot_total_timed_out_access_requests", "total count of timed out access requests"),
            MetricGaugeType.TOTAL_PENDING_REQUESTS: Gauge("accessbot_total_pending_access_requests", "total count of pending access requests"),
            MetricGaugeType.TOTAL_CONSECUTIVE_ERRORS: Gauge("accessbot_total_consecutive_errors", "total count of consecutive errors"),
        }

    def __update_metric(self, gauge_type: MetricGaugeType, value: int):
        if self._metrics is None:
            return
        self._metrics[gauge_type].set(value)

    def __increment_metrics(self, gauge_types: List[MetricGaugeType]):
        if self._metrics is None:
            return
        for gauge_type in gauge_types:
            self._metrics[gauge_type].inc()

    def __decrement_metric(self, gauge_type: MetricGaugeType):
        if self._metrics is None:
            return
        self._metrics[gauge_type].dec()

    def increment_access_requests(self):
        self.__increment_metrics([MetricGaugeType.TOTAL_RECEIVED_MESSAGES, MetricGaugeType.TOTAL_ACCESS_REQUESTS])

    def increment_consecutive_errors(self):
        self.__increment_metrics([MetricGaugeType.TOTAL_CONSECUTIVE_ERRORS])

    def reset_consecutive_errors(self):
        self.__update_metric(MetricGaugeType.TOTAL_CONSECUTIVE_ERRORS, 0)

    def increment_received_messages(self):
        self.__increment_metrics([MetricGaugeType.TOTAL_RECEIVED_MESSAGES])

    def increment_pending_requests(self):
        self.__increment_metrics([MetricGaugeType.TOTAL_PENDING_REQUESTS])

    def decrement_pending_requests(self):
        self.__decrement_metric(MetricGaugeType.TOTAL_PENDING_REQUESTS)

    def increment_manual_denials(self):
        self.__increment_metrics([MetricGaugeType.TOTAL_MANUAL_DENIALS])

    def increment_timed_out_requests(self):
        self.__increment_metrics([MetricGaugeType.TOTAL_TIMED_OUT_REQUESTS])

    def increment_manual_approvals(self):
        self.__increment_metrics([MetricGaugeType.TOTAL_MANUAL_APPROVALS])

    def increment_auto_approvals(self):
        self.__increment_metrics([MetricGaugeType.TOTAL_AUTO_APPROVALS])
