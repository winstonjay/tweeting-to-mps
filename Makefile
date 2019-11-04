# connect and upload to ec2 instances
INSTANCE:="$(AWS_EC2_USER)@$(AWS_EC2_INSTANCE)"

run_local:
	python3 twitter-listener/listen.py data/mp/sample -n 10 -o data/tmp

deploy_ec2:
	python3 bin/sample.py > data/mp/sample
	scp -i $(AWS_EC2_PEM) data/mp/sample "$(INSTANCE):sample"
	scp -i $(AWS_EC2_PEM) twitter-listener/listen.py "$(INSTANCE):listen.py"
	scp -i $(AWS_EC2_PEM) twitter-listener/listen.service "$(INSTANCE):/etc/systemd/system/listen.service"
	ssh -i $(AWS_EC2_PEM) -t $(INSTANCE) \
		"sudo systemctl daemon-reload && \
		sudo systemctl restart listen && \
		sudo systemctl status listen"

ssh_ec2:
	ssh -i $(AWS_EC2_PEM) $(INSTANCE)

check_ec2:
	ssh -i $(AWS_EC2_PEM) -t $(INSTANCE) "df -h && ls data/ | wc -l && sudo systemctl status listen"

stop_ec2:
	ssh -i $(AWS_EC2_PEM) -t $(INSTANCE) "sudo systemctl stop listen"
