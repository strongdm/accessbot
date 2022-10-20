# Deploy AccessBot on Fargate

## Creating an ECS Task Definition

To deploy AccessBot on Fargate, first we need to configure a Task Definition following the next steps:

1. Go to [AWS ECS Task Definitions](https://console.aws.amazon.com/ecs/home#/taskDefinitions)

2. Click on `Create new Task Definition`:

![image](https://user-images.githubusercontent.com/49597325/181511876-7a4ac807-e680-4479-bd13-879c68c685e4.png)

3. Select the `Fargate` option and click on `Next Step`:

![image](https://user-images.githubusercontent.com/49597325/181512386-37dc5738-57f0-4ae0-9c28-71e3d2b9f38b.png)

4. Fill the following fields of the first three sections of the step 2. The following screenshot is showing the minimum configuration that should be used:

![image](https://user-images.githubusercontent.com/49597325/181513181-f2a7af18-75d1-4499-ad54-93c1bef5e157.png)

Note: The `Operating system family` should be `Linux`.

5. Find the "Volumes" section and click on `Add volume`

![image](https://user-images.githubusercontent.com/49597325/181517987-856e8092-2f23-4b68-bca4-ee534420e265.png)

6. In the `Add volume` modal, choose a name for the volume, select the EFS option as the volume type, select the File System ID and click on `Add`:

![image](https://user-images.githubusercontent.com/49597325/181519043-4356315b-3ce5-4399-9313-46b9f7331814.png)

Note: If you don't have a File System ID, click on [Amazon EFS console](https://console.aws.amazon.com/efs/home#/file-systems) link and create one. 

7. Find the section `Container definitions` and click on `Add container`:

![image](https://user-images.githubusercontent.com/49597325/181514703-ddeb0927-8ab0-4a36-ae54-5d0dd9d512b4.png)

8. In the side sheet, in the beginning, define a container name and paste the public ecr AccessBot image URL:

![image](https://user-images.githubusercontent.com/49597325/181515486-f1bc0eee-94e6-48eb-96da-0b93b54c0d9b.png)

9. Now, in the `Environment` section, feel free to configure it the way you like. But here are the minimum environment variables that should be configured:

![image](https://user-images.githubusercontent.com/49597325/181516509-37418164-2dc4-4f71-a7c3-2fdc4de26e5a.png)

Note: The `SDM_ENABLE_BOT_STATE_HANDLING` is essential if you want to use manual approvals. For more information, please refer to the [CONFIGURE_ACCESSBOT](../configure_accessbot/CONFIGURE_ACCESSBOT.md#bot-configuration) docs

10. In the `Storage and Logging` section, select the created volume and type "/errbot/data/grant_requests" in the `Container Path`

![image](https://user-images.githubusercontent.com/49597325/181521910-eab36533-b325-4947-9882-68176b45832b.png)

11. Then, in the bottom of the side sheet, click on `Add`

12. And finally, click on the `Create` button at the bottom of the page

## Creating an ECS Cluster

Now we need to create a cluster for the Fargate instance following the next steps:

1. Go to [Clusters](https://console.aws.amazon.com/ecs/home#/clusters)

2. Click on "Create Cluster":

![image](https://user-images.githubusercontent.com/49597325/181523823-d000e795-160d-4639-ac36-2b15c5e64662.png)

3. Select the `Network only` option and click on `Next Step`:

![image](https://user-images.githubusercontent.com/49597325/181524363-1c775903-a77a-4340-b627-41d0d0fbb29f.png)

4. Choose a name for the Cluster and click on `Create`:

![image](https://user-images.githubusercontent.com/49597325/181524619-fe0665ba-df12-4109-b79d-89b61f9a98e4.png)

5. You'll be redirected to the Created Cluster page.

## Creating an ECS Cluster Service

An ECS Cluster Service create tasks from a Task Definition revision. When the task goes down, the service will provision another one as a Replica.

To create a service, follow the steps below:

1. In the created cluster page, under the `Services` tab, click on `Create`:

![image](https://user-images.githubusercontent.com/49597325/181525424-9fc9d21b-541d-439a-874e-3e76938e534b.png)

2. In the `Create Service` page, select the Fargate option, choose a service name and set the number of tasks to 1:

![image](https://user-images.githubusercontent.com/49597325/181530351-0c4b99e3-18f0-4f65-bfea-a2a9acea931a.png)

3. At the bottom of the page, click on `Next step`

4. At the top of the page, select a Cluster VPC, a Subnet and select the same Security Group used on the created EFS volume:

![image](https://user-images.githubusercontent.com/49597325/181533405-6bafe115-d3fd-4949-b182-7debd1fcc094.png)

**Note**: make sure the EFS and the cluster service being created belongs to the same Security Group, because both resources must communicate with other. Without that your container might not even start because it'll not find the volume.

5. Then, at the bottom of the page, click on `Next step`

6. There's no need to set any Auto Scaling configuration, just click on `Next step`:

![image](https://user-images.githubusercontent.com/49597325/181540192-ce3fbf50-a920-40d9-ac1b-e53ed241a2b0.png)

7. On the `Preview` page, just click on `Create service`. Then, when it finishes, click on `View service`

8. Now, just wait the service to provision a task and wait its status to become `running`. When that happens, just wait a couple more seconds and AccessBot should be ready to use:

![image](https://user-images.githubusercontent.com/49597325/181546558-29fae719-1ebf-47e6-b069-2bd6ae89a0fe.png)
