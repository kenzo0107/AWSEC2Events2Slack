# -*- coding: utf-8 -*-

import os
import slackpy
import boto3
from datetime import datetime, date, timezone, timedelta

slack = slackpy.SlackLogger(
    os.environ['SLACK_INCOMING_WEBHOOK'],
    os.environ['SLACK_CHANNEL'],
    os.environ['SLACK_USERNAME'],
    os.environ['SLACK_ICON_URL']
)
slack.set_log_level(slackpy.LogLv.DEBUG)

def lambda_handler(event, context):
    account_id = context.invoked_function_arn.split(":")[4]
    print("Account ID=" + account_id)

    slack_message =''
    ec2 = boto3.client('ec2')
    instance_statuses = ec2.describe_instance_status()['InstanceStatuses']
    for i in instance_statuses:
        instance_events = i.get('Events')
        if instance_events is None:
            continue

        instance_id = i['InstanceId']

        tags = ec2.describe_instances(
            InstanceIds=[
                instance_id
            ]
        )['Reservations'][0]['Instances'][0].get('Tags')

        if tags is None:
            instance_name_tag = 'NoNameTag'
        else:
            for j in tags:
                if j['Key'] == 'Name':
                    instance_name_tag = j['Value']

        # 通知用メッセージ作成
        for k in i['Events']:
            description = k.get('Description')
            index = description.find("[Completed]")

            # Description に [Completed] が含まれる場合はスキップ
            if index != -1:
                continue

            not_before = k.get('NotBefore')
            if not_before is not None:
                not_before = not_before + timedelta(hours=9)
                not_before = format(not_before.strftime("%Y-%m-%d %H:%M:%S")) + ' (JST)'
            else:
                not_before = "no specified"

            not_after  = k.get('NotAfter')
            if not_after is not None:
                not_after = not_after + timedelta(hours=9)
                not_after = format(not_after.strftime("%Y-%m-%d %H:%M:%S")) + ' (JST)'
            else:
                not_after = "no specified"

            slack_message = slack_message \
                + '```' \
                + '* ' + instance_name_tag + '(' + instance_id + ')\n' \
                + '[Code] ' + k.get('Code') + '\n' \
                + '[Description] ' + k.get('Description') + '\n' \
                + '[NotBefore]   ' + not_before + ' \n' \
                + '[NotAfter]    ' + not_after + ' \n' \
                + '``` \n\n'

    if slack_message:
        slack_message = u'AWS Scheduled Events `(' + account_id + ')` \n\n' + slack_message
        res = slack.error(message=slack_message, title="AWS Scheduled Events Notification")
    return
