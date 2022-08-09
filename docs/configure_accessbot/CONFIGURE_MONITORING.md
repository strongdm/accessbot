# CONFIGURE MONITORING

To enable monitoring you need to set the variable `SDM_EXPOSE_METRICS=true`.

After enabling it, a metrics endpoint will available at port `3142`. There you can see the following metrics:
- `accessbot_total_received_messages` - total count of received messages
- `accessbot_total_access_requests` - total count of received access requests messages
- `accessbot_total_pending_access_requests` - total count of pending access requests
- `accessbot_total_manual_approvals` - total count of manually approved access requests
- `accessbot_total_auto_approvals` - total count of auto approved access requests
- `accessbot_total_denied_access_requests` - total count of manually denied access requests
- `accessbot_total_timed_out_access_requests` - total count of timed out access requests
- `accessbot_total_consecutive_errors` - total count of consecutive errors

To see an example, follow these steps:
1. Download the file [docker-compose-prometheus.yaml](../../docker-compose-prometheus.yaml);
  - Make sure that your `env-file` is properly configured following the `env-file.example` template
2. Run with your preferred container orchestrator (with docker, you can simply run `docker-compose -f docker-compose-prometheus.yaml up`)

Now you can go to the **AccessBot Metrics** Grafana Dashboard in `http://localhost:3000/d/982GyKX7z/accessbot-metrics` and see the following charts:

1 - Received Messages Count (`accessbot_total_received_messages` metric):

![image](https://user-images.githubusercontent.com/49597325/168816013-b71ff2b5-be8b-45ea-9a58-4cec4e51cb53.png)

2 - Access Requests Count (`accessbot_total_access_requests` metric):

![image](https://user-images.githubusercontent.com/49597325/168816036-f51baf75-67ed-4735-be77-51e2f9ce379a.png)

3 - Pending Access Requests Count (`accessbot_total_pending_access_requests` metric):

![image](https://user-images.githubusercontent.com/49597325/168816111-8b330af8-110c-4dc4-96f2-6ff554e6703b.png)

4 - Manually Approved Access Requests Count (`accessbot_total_manual_approvals` metric):

![image](https://user-images.githubusercontent.com/49597325/168816119-344c8c2c-ddad-4008-a5c6-4ee8c02fb66f.png)

5 - Auto Approved Access Requests Count (`accessbot_total_auto_approvals` metric):

![image](https://user-images.githubusercontent.com/49597325/168816132-755b62f2-da7c-49ab-9c7f-bf20b5b0162b.png)

6 - Manually Denied Access Requests Count (`accessbot_total_denied_access_requests` metric):

![image](https://user-images.githubusercontent.com/49597325/168816152-1ffbffe7-128e-475a-9ba4-2971431c380d.png)

7 - Timed Out Access Requests Count (`accessbot_total_timed_out_access_requests` metric):

![image](https://user-images.githubusercontent.com/49597325/168816166-8deb901e-ccfd-4101-9ae7-8e290f429ea6.png)

8 - Total Consecutive Errors Count (`accessbot_total_consecutive_errors` metric):

![image](https://user-images.githubusercontent.com/49597325/168816189-a559a694-2790-49be-87a0-1d06f4a73cb4.png)

9 - Last Execution Status (`accessbot_total_consecutive_errors` metric - 0 means that everything is fine, 1 means that the last execution(s) failed):

![image](https://user-images.githubusercontent.com/49597325/168816198-c76173b2-cb18-4799-9590-d7405bf5496f.png)
