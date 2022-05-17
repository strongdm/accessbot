# CONFIGURE MONITORING

To enable monitoring you need to set the variable `SDM_EXPOSE_METRICS=true`.

After enabling it, a metrics endpoint will available at port `3142`. There you can see the following metrics:
- `accessbot_total_received_messages` - total count of received messages
- `accessbot_total_access_requests` - total count of received access requests messages
- `accessbot_total_pending_access_requests` - total count of pending access requests
- `accessbot_total_manual_approves` - total count of manually approved access requests
- `accessbot_total_auto_approves` - total count of auto approved access requests
- `accessbot_total_denied_access_requests` - total count of manually denied access requests
- `accessbot_total_timed_out_access_requests` - total count of timed out access requests
- `accessbot_total_consecutive_errors` - total count of consecutive errors

To see an example, follow these steps:
1. Download the file [docker-compose-prometheus.yaml](../../docker-compose-prometheus.yaml);
  - Make sure that your `env-file` is properly configured following the `env-file.example` template
2. Run with your preferred container orchestrator (with docker, you can simply run `docker-compose -f docker-compose-prometheus.yaml up`)

Now you can go to the **AccessBot Metrics** Grafana Dashboard in `http://localhost:3000/d/982GyKX7z/accessbot-metrics` and see the following charts:

1 - Received Messages Count (`accessbot_total_received_messages` metric):

2 - Access Requests Count (`accessbot_total_access_requests` metric):

3 - Pending Access Requests Count (`accessbot_total_pending_access_requests` metric):

4 - Manually Approved Access Requests Count (`accessbot_total_manual_approves` metric):

5 - Auto Approved Access Requests Count (`accessbot_total_auto_approves` metric)

6 - Manually Denied Access Requests Count (`accessbot_total_denied_access_requests` metric)

7 - Timed Out Access Requests Count (`accessbot_total_timed_out_access_requests` metric)

8 - Total Consecutive Errors Count (`accessbot_total_consecutive_errors` metric)

9 - Last Execution Status (`accessbot_total_consecutive_errors` metric)
