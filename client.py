from aws import AWS
import json

aws = AWS()
my_topic=input('Input topic name: ')


# Create/find queue (queue will be used, but not created if it already exists)
aws.create_queue(my_topic + '_queue')

# Create topic
aws.create_topic(my_topic)

# Add policy to queue
aws.add_policy()

# Subscribe to my topic
aws.subscribe_to_topic()

o_topic=input('Who would you like to speak with? ')
rt = aws.register_target(o_topic)

while True:
    # Retrieve and print and remove any pending messages
    payload = aws.receive_message()
    if payload:
        try:
            for msg in payload['Messages']:
                receipthandle=msg['ReceiptHandle']
                msg=json.loads(msg['Body'])
                if 'Message' in msg:
                    msg=msg['Message']

                    print ("+++++++++++++++++++++++++++++++++++++++++++++++")
                    print (msg)
                    print ("+++++++++++++++++++++++++++++++++++++++++++++++")
                    aws.delete_message(receipthandle=receipthandle)
        except KeyError:
            pass
    # Remove message from queue after procesing
    
    try:
        msg = input('What would you like to say: ')
    except KeyboardInterrupt:
        aws.delete_topic()
        aws.delete_queue()
        print("\nProcess complete")
        break

    if msg:
        try:
            aws.send_message(msg, o_topic)
        except:
            print ("Error sending message try again later.")

