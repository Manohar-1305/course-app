from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from flask import flash, redirect, render_template, request, url_for
import logging
app = Flask(__name__)


# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.before_request
def log_request_info():
    logging.info(f"Request: {request.method} {request.path}")

@app.after_request
def log_response_info(response):
    logging.info(f"Response: {response.status} for {request.path}")
    return response

app.secret_key = os.urandom(24)

# In-memory user storage (for demonstration only)
users = {"admin": "password123"}

# Route for the login page
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('welcome'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user exists
        if username in users:
            # Check if the password is correct
            if users[username] == password:
                session['username'] = username
                return redirect(url_for('welcome'))
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('User not found. Please register.', 'danger')  # Show message on the same page

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists. Choose a different username.', 'danger')  # 'danger' for error
        else:
            users[username] = password
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        if 'save_details' in request.form:
            email = request.form.get('email')
            phone = request.form.get('phone')

            if not email or not phone:
                flash('Please fill in all required fields.', 'danger')
                return redirect(url_for('welcome'))

            # Save details in session
            session['details_saved'] = True
            session['email'] = email
            session['phone'] = phone
            flash('Details saved successfully!', 'success')
            return redirect(url_for('welcome'))  # Reload page to show the subscribe button

        elif 'subscribe' in request.form:
            session['subscribed'] = True
            flash('Subscription successful! Please view the course.', 'success')
            return redirect(url_for('course'))  # Redirect to course page after subscription

    return render_template(
        'welcome.html',
        username=session['username'],
        details_saved=session.get('details_saved', False),
        subscribed=session.get('subscribed', False)
    )

@app.route('/course')
def course():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if 'subscribed' not in session or not session['subscribed']:
        flash('Please subscribe to access the course.', 'danger')
        return redirect(url_for('subscribe'))  # Redirect to subscription page if not subscribed

    return render_template('course.html')  # Render the course page

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    if request.method == 'POST':
        # Store the subscription status in the session
        session['subscribed'] = True
        flash('Subscription successful! Please view the course.', 'success')
        return redirect(url_for('course'))  # Redirect to course page after subscription
    
    return render_template('subscription.html')

# Route for the home page
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    # Check if the user is subscribed
    if 'subscribed' in session and session['subscribed']:
        subscribed_message = "You are subscribed. Please view the course."
    else:
        subscribed_message = "Please subscribe to access the course."
    
    return render_template('home.html', username=session['username'], subscribed_message=subscribed_message)

# Route to log out
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/vpc-creation')
def vpc_creation():
    return render_template('vpc-creation.html')

@app.route('/1.vpc-provider.html')
def vpc_provider():
    return render_template('vpc-provider.html')

@app.route('/public_subnet')
def public_subnet():
    return render_template('public_subnet.html')


@app.route('/public_route')
def public_route():
    return render_template('public_route.html')

@app.route('/private_subnet')
def private_subnet():
    return render_template('private_subnet.html')

@app.route('/private_route')
def private_route():
    return render_template('private_route.html')

@app.route('/IAMCReation')
def IAMCReation():
    return render_template('IAMCReation.html')

@app.route('/natgateway')
def natgateway():
    return render_template('natgateway.html')

@app.route('/securitygroup')
def securitygroup():
    return render_template('security-group_1.html')


@app.route('/instancecreation')
def instancecreation():
    return render_template('instance_creation.html')

@app.route('/instance_nfs_creation')
def instance_nfs_creation():
    return render_template('instance_nfs_creation.html')

@app.route('/instance_master_worker_creation')
def instance_master_worker_creation():
    return render_template('instance_master_worker_creation.html')

@app.route('/terraform_output')
def terraform_output():
    return render_template('terraform_output.html')  # Replace with the correct template

@app.route('/terraform_enviroment_creation')
def terraform_enviroment_creation():
    # Render a template or perform logic for this endpoint
    return render_template('terraform_enviroment_creation.html')  # Ensure this template exists

@app.route('/terraform_user_data_bastion')
def terraform_user_data_bastion():
    return render_template('terraform_user_data_bastion.html')

@app.route('/terraform_user_data_nfs')
def terraform_user_data_nfs():
    # Replace with appropriate logic
    return render_template('terraform_user_data_nfs.html')

@app.route('/terraform_user_data_loadbalancer')
def terraform_user_data_loadbalancer():
    # Replace with appropriate logic
    return render_template('terraform_user_data_loadbalancer.html')


@app.route('/terraform_user_data_master')
def terraform_user_data_master():
    # Replace with appropriate logic
    return render_template('terraform_user_data_master.html')

@app.route('/terraform_null_provisioner')
def terraform_null_provisioner():
    # Replace with appropriate logic
    return render_template('terraform_null_provisioner.html')

@app.route('/terraform_variables')
def terraform_variables():
    # Replace with appropriate logic
    return render_template('terraform_variables.html')
@app.route('/terraform_infra_creation')
def terraform_infra_creation():
    # Replace with appropriate logic
    return render_template('terraform_infra_creation.html')
@app.route('/creating_inventory_creation')
def creating_inventory():
    # Replace with appropriate logic
    return render_template('creating_inventory.html')
@app.route('/changes_in_inventory')
def changes_in_inventory():
    # Replace with appropriate logic
    return render_template('changes_in_inventory.html')
@app.route('/git_code')
def git_code():
    # Replace with appropriate logic
    return render_template('git_code.html')

@app.route('/ansible_inventory_code')
def ansible_inventory_code():
    # Replace with appropriate logic
    return render_template('ansible_inventory_code.html')

@app.route('/ansible_k8s_setup')
def ansible_k8s_setup():
    # Replace with appropriate logic
    return render_template('ansible_k8s_setup.html')

@app.route('/ansible_kubernetes_role')
def ansible_kubernetes_role():
    # Replace with appropriate logic
    return render_template('ansible_kubernetes_role.html')

@app.route('/terraform_overall_summary')
def terraform_overall_summary():
    # Replace with appropriate logic
    return render_template('terraform_user_data_master.html')

@app.route('/elasticip_lb')
def elasticip_lb():
    # Replace with appropriate logic
    return render_template('elasticip.html')
#################################################################
@app.route('/helm_role')
def helm_role():
    # Replace with appropriate logic
    return render_template('helm_role.html')

@app.route('/first_master_role')
def first_master_role():
    # Replace with appropriate logic
    return render_template('first_master_role.html')

@app.route('/add_master_role')
def add_master_role():
    # Replace with appropriate logic
    return render_template('add_master_role.html')

@app.route('/add_workers_role')
def add_workers_role():
    # Replace with appropriate logic
    return render_template('add_workers_role.html')

@app.route('/time_sync_role')
def time_sync_role():
    # Replace with appropriate logic
    return render_template('time_sync_role.html')

@app.route('/kubectl_role')
def kubectl_role():
    # Replace with appropriate logic
    return render_template('kubectl_role.html')

@app.route('/adding_tags')
def adding_tags():
    # Replace with appropriate logic
    return render_template('adding_tags.html')
@app.route('/cni_role')
def cni_role():
    # Replace with appropriate logic
    return render_template('cni_role.html')

@app.route('/add_masters_label')
def add_masters_label():
    # Replace with appropriate logic
    return render_template('add_masters_label.html')
@app.route('/add_workers_label')
def add_workers_label():
    # Replace with appropriate logic
    return render_template('add_workers_label.html')
@app.route('/nfs_setup')
def nfs_setup():
    # Replace with appropriate logic
    return render_template('nfs_setup.html')

@app.route('/nfs_client_setup')
def nfs_client_setup():
    # Replace with appropriate logic
    return render_template('nfs_client_setup.html')

@app.route('/K8s_installer')
def K8s_installer():
    # Replace with appropriate logic
    return render_template('K8s_installer.html')

@app.route('/cluster_setup')
def cluster_setup():
    # Replace with appropriate logic
    return render_template('cluster_setup.html')

@app.route('/bastion_eip')
def bastion_eip():
    # Replace with appropriate logic
    return render_template('bastion_eip.html')

@app.route('/aws_controller_role')
def aws_controller_role():
    # Replace with appropriate logic
    return render_template('aws_controller_role.html')

@app.route('/label_master')
def label_master():
    # Replace with appropriate logic
    return render_template('label_master.html')

@app.route('/reverse_proxy')
def reverse_proxy():
    # Replace with appropriate logic
    return render_template('reverse_proxy.html')

@app.route('/modification')
def modification():
    # Replace with appropriate logic
    return render_template('modification.html')

@app.route('/loadbalancer_svc')
def loadbalancer_svc():
    # Replace with appropriate logic
    return render_template('loadbalancer_svc.html')
@app.route('/mapping_domain')
def mapping_domain():
    # Replace with appropriate logic
    return render_template('mapping_domain.html')
#######################################
@app.route('/provider_blog')
def provider_blog():
    # Replace with appropriate logic
    return render_template('vpc_provider_blog.html')

@app.route('/vpc_creation_blog')
def vpc_creation_blog():
    # Replace with appropriate logic
    return render_template('vpc_creation_blog.html')

@app.route('/terraform_public_subnet_blog')
def terraform_public_subnet_blog():
    # Replace with appropriate logic
    return render_template('terraform_public_subnet_blog.html')

#############################################################
@app.route('/eks_vpc_creation')
def eks_vpc_creation():
    # Replace with appropriate logic
    return render_template('eks_vpc_creation.html')

@app.route('/eks_public_subnet')
def eks_public_subnet():
    # Replace with appropriate logic
    return render_template('eks_public_subnet.html')

@app.route('/eks_private_subnet')
def eks_private_subnet():
    # Replace with appropriate logic
    return render_template('eks_private_subnet.html')

@app.route('/iam_role_cluster')
def iam_role_cluster():
    # Replace with appropriate logic
    return render_template('iam_role_cluster.html')

@app.route('/iam_role_nodegroup')
def iam_role_nodegroup():
    # Replace with appropriate logic
    return render_template('iam_role_nodegroup.html')

@app.route('/eks_cluster_creation')
def eks_cluster_creation():
    # Replace with appropriate logic
    return render_template('eks_cluster_creation.html')

@app.route('/eks_nodegroup_creation')
def eks_nodegroup_creation():
    # Replace with appropriate logic
    return render_template('eks_nodegroup_creation.html')

@app.route('/eks_bastion_creation')
def eks_bastion_creation():
    # Replace with appropriate logic
    return render_template('eks_bastion_creation.html')

@app.route('/code_review')
def code_review():
    # Replace with appropriate logic
    return render_template('code_review.html')

@app.route('/health')
def health_check():
    return 'OK', 200
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

