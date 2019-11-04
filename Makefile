# connect and upload to ec2 instances
INSTANCE:="$(AWS_EC2_USER)@$(AWS_EC2_INSTANCE)"

local:
	python3 twitter-listener/listen.py data/mp/mp_list.json -n 10 -o data/tmp

deploy:
	python3 bin/getlist.py
	scp -i $(AWS_EC2_PEM) data/mp/mp_list.json "$(INSTANCE):mp_list.json"
	scp -i $(AWS_EC2_PEM) twitter-listener/listen.py "$(INSTANCE):listen.py"
	scp -i $(AWS_EC2_PEM) twitter-listener/listen.service "$(INSTANCE):/etc/systemd/system/listen.service"
	ssh -i $(AWS_EC2_PEM) -t $(INSTANCE) \
		"sudo systemctl daemon-reload && \
		sudo systemctl restart listen && \
		sudo systemctl status listen"

ssh:
	ssh -i $(AWS_EC2_PEM) $(INSTANCE)

check:
	ssh -i $(AWS_EC2_PEM) -t $(INSTANCE) "df -h && ls data/ | wc -l && sudo systemctl status listen"
