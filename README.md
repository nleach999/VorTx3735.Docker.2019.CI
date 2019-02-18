# Continuous Integration (CI) with Docker, AWS CodeBuild, and Slack
Greetings from the [VorTX 3735](http://www.vortx3735.org/ "VorTX 3735") FRC Robotics Team in Houston, TX!

If you have ever experienced members of your team checking in code that will not build on any other team member's box, a [Continuous Integration (CI)](https://en.wikipedia.org/wiki/Continuous_integration) build is for you!

The concept is simple: every time someone checks in a code change, the code is downloaded and a build is performed.  If the build is successful,
no one notices the build occurred.  If there is a failure, a notification with a build log is posted to your team's Slack channel.  The breaking change can
be rolled back or a fix can be checked in for another build attempt.

# How does it work?

If you want to build your code, there must be a computer available that can monitor the source control repository, perform the checkout, and execute the build.  Dedicating a machine for this purpose is not always feasible for a variety of reasons, so this uses the [Amazon Web Services (AWS) CodeBuild](https://aws.amazon.com/codebuild/) to allocate resources that perform all the build activities only when a change is checked into the source control repository.

This example uses GitHub as the source control repository and AWS CodeBuild as the build infrastructure.  This does not mean this Docker image is limited to working in AWS; other cloud services provide similar capabilities thus the image may be utilized in Azure, Google Cloud, and so forth.  Build notifications are sent to a team's Slack channel.  If there is interest in other types of integrations, there are a variety of ways to make your own custom image.

All the cloud services charge for the code build service.  It is relatively inexpensive; AWS, for example, has a free tier that may cover all build activities for some teams.  For the VorTX 3735 team, the first month cost $0.26 USD to cover builds on two repositories.

# Step-by-Step Instructions

This section will cover step-by-step instructions for configuring the CI build for AWS with GitHub and Slack. 

Prerequisites:

- Administrative access on an AWS account
- Administrative access for a channel on Slack
- A GitHub repository; administrative access may only be required for private repositories

Unless there is a need to change the Docker image, making this work requires only configuration of AWS CodeBuild and Slack.

## Step 1: Configure Slack

Add a Slack channel, in this case I named mine `ci_demo`.


![Slack Channel](images/SlackChannel.png "Slack Channel")


Now select `Administration->Manage Apps` so you can add the notification application to your Slack account.

![Slack Manage Apps](images/SlackManageApps.png "Slack Manage Apps")

Search for **Incoming WebHooks** and click on the tile to configure the application.

![Slack Incoming WebHooks](images/SlackWebHook.png "Slack Incoming WebHooks")

Click "Add Configuration"

![Slack WebHook Config](images/SlackWebHookConfig.png "Slack WebHook Config")

Choose the channel where the notifications will appear.  I selected the `ci_demo` channel I made earlier.

![Slack Channel](images/SlackChooseChannel.png "Slack Channel")

Select `Add Incoming WebHooks Integration`

![Slack Add Configuration](images/SlackAddConfiguration.png "Slack Add Configuration")

You can review the integration settings to change the name used by the web hook, the icon displayed next to notifications, etc.  The important part to note is in the **Integration Settings** section.  Scroll down to the **Integration Settings** section and note the `Webhook URL`.  The value of the `Webhook URL` will be used to configure the Docker build image. Click **Save Settings** at the bottom of the configuration page to ensure that the webhook is properly configured.

![Slack URL](images/SlackWebhookURL.png "Slack URL")

## Step 2: Configure AWS CodeBuild
