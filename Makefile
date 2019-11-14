# connect and upload to ec2 instances
INSTANCE:="$(AWS_EC2_USER)@$(AWS_EC2_INSTANCE)"

run_local:
	python3 twitter-listener/listen.py data/mp/sample -n 10 -o data/tmp

mp_list:
	python3 bin/getlist.py

mp_sample:
	python3 bin/sample.py > data/mp/sample

tweet_text_sample:
	python3 data/twitter/data.zip data/mp/sample

deploy_ec2:
	scp -i $(AWS_EC2_PEM) data/mp/sample "$(INSTANCE):sample"
	scp -i $(AWS_EC2_PEM) twitter-listener/listen.py "$(INSTANCE):listen.py"
	scp -i $(AWS_EC2_PEM) twitter-listener/listen.service "$(INSTANCE):/etc/systemd/system/listen.service"
	ssh -i $(AWS_EC2_PEM) -t $(INSTANCE) "sudo systemctl daemon-reload && sudo systemctl restart listen"

ssh_ec2:
	ssh -i $(AWS_EC2_PEM) $(INSTANCE)

check_ec2:
	ssh -i $(AWS_EC2_PEM) -t $(INSTANCE) "$$(cat bin/ec2check)"

stop_ec2:
	ssh -i $(AWS_EC2_PEM) -t $(INSTANCE) "sudo systemctl stop listen"
