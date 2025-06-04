# Python AWS RDS (MySQL Free Tier) End-to-End PoC

## Description
This is a simple Proof of Concept (PoC) demonstrating an end-to-end flow of a Python application connecting to an AWS RDS for MySQL instance (utilizing the Free Tier). The script performs basic database operations: dropping an existing table, creating a new table, inserting sample data, and retrieving that data.

This project is intended to showcase basic AWS RDS and Python integration skills.

## Prerequisites
Before you begin, ensure you have the following:
1.  **AWS Account:** With access to the AWS Management Console and eligibility for the RDS Free Tier (typically for new accounts for 12 months).
2.  **Python:** Version 3.7 or higher installed on your local machine.
3.  **pip:** Python package installer, usually comes with Python.
4.  **Git:** (Optional) If you clone this repository.

## Setup Instructions

### 1. AWS RDS (MySQL Free Tier) Instance Setup
   * **Create an RDS Instance:**
     * Log in to your AWS Management Console and navigate to the RDS service.
     * Click "Create database".
     * Choose "Standard Create" and select "MySQL" as the engine type.
     * **Crucially, select the "Free tier" template.** This will pre-fill settings eligible for the free tier.
     * **Instance Configuration:** Verify a free tier eligible instance class is selected (e.g., `db.t3.micro`).
     * **Storage:** Usually 20 GB of General Purpose SSD (gp2) is included in the Free Tier. Disable storage autoscaling if you want to strictly stay within limits.
     * **Settings:** Define a `DB instance identifier`, `Master username`, and `Master password`. **Securely note these credentials.**
     * **Connectivity:**
        * **Public access:** Select "**Yes**".
        * **VPC security group (firewall):** After the instance is created (or during setup if advanced options are chosen), you **must** configure the inbound rules for its security group to allow traffic from **Your IP address** on the **MySQL port (3306)**.
            1. Go to the RDS instance details -> "Connectivity & security" tab.
            2. Click on the active VPC security group.
            3. Go to its "Inbound rules" tab and click "Edit inbound rules".
            4. Click "Add rule".
            5. Set **Type** to "MYSQL/Aurora" (which defaults to TCP, Port 3306).
            6. Set **Source** to "**My IP**" (AWS will auto-fill your current public IP address).
            7. Save the rules.
        * **Initial database name:** It's recommended to specify an "Initial database name" during RDS setup (e.g., `rdspocdb`). This will be the value for `DB_NAME_POC`.
   * **Note Down Credentials:** After the instance status is "Available", note down the following:
        * **Endpoint:** (e.g., `your-rds-instance-name.xxxxxxxxxxxx.region.rds.amazonaws.com`)
        * **Port:** (Default for MySQL is 3306)
        * **Master Username**
        * **Master Password**
        * **Database Name** (the initial database name you set)

### 2. Local Environment Setup
   1. **Clone the Repository (if applicable):**
      ```bash
      git clone <your-repository-url>
      cd <repository-name>
      ```
   2. **Create and Activate a Virtual Environment (Recommended):**
      ```bash
      python -m venv venv
      ```
   3. **Install Dependencies:**
      ```bash
      pip install -r requirements.txt
      ```

### 3. Configure Environment Variables
   This script uses a `.env` file to load database credentials.
   1. Create a file named `.env` in the root directory of this project (the same directory as `rds_freetier_poc.py`).
   2. Add the following content to your `.env` file, replacing the placeholder values with your actual RDS instance details:
      ```env
      DB_HOST_POC="your-rds-instance-endpoint.rds.amazonaws.com"
      DB_USER_POC="your_rds_master_username"
      DB_PASSWORD_POC="your_rds_master_password"
      DB_NAME_POC="your_initial_database_name"
      ```
   **Important:** If you are using Git, ensure that `.env` is added to your `.gitignore` file to prevent committing sensitive credentials.

### 4. Running the Proof of Concept
Once the setup is complete, run the Python script from your terminal:
```bash
python rds_freetier_poc.py
```
### 5. Script Functionality
The Python script (`rds_freetier_poc.py`) will perform the following actions:
1.  Load database connection details from the `.env` file.
2.  Connect to the configured AWS RDS MySQL instance.
3.  If the connection is successful, it will:
    * Drop the `tech_consultants` table if it already exists (to ensure a clean state for each run).
    * Recreate the `tech_consultants` table with a predefined schema (`id`, `name`, `specialty`).
    * Insert a few sample records into the `tech_consultants` table.
    * Retrieve all records from the `tech_consultants` table.
    * Print the retrieved records to the console.
4.  Finally, it will close the database connection.

## Expected Output
The script will print messages to the console indicating:
* The status of the database connection.
* Confirmation of table dropping and creation.
* Confirmation of each data insertion.
* A formatted list of the data retrieved from the `tech_consultants` table. Since the table is recreated on each run, you will only see the records inserted during that specific execution.



## ❗ Important: AWS Resource Cleanup
After you have finished with this PoC, reviewed its functionality, and demonstrated it, please remember to **DELETE your AWS RDS instance** to avoid incurring any unexpected charges. This is especially crucial if your AWS Free Tier period expires or if your usage exceeds the Free Tier limits.

To delete the RDS instance:
1.  Navigate to the AWS RDS console.
2.  Select the DB instance you created for this PoC.
3.  Click on "Actions" -> "Delete".
4.  You will likely be asked if you want to create a final snapshot. For a PoC, you can typically skip this to save costs (uncheck the option or choose not to create one). You will then need to confirm the deletion by typing "delete me" or similar.

## Disclaimer
This project is a Proof of Concept (PoC) created for demonstration and learning purposes only. It is **not intended for use in a production environment** without significant further development and enhancements. Key areas that would require attention for production use include, but are not limited to:
* **Security:** Implementing robust security measures such as least-privilege IAM roles, network segmentation beyond basic security groups, encryption at rest and in transit handled appropriately, and secure credential management (e.g., AWS Secrets Manager instead of `.env` files for application deployment).
* **Error Handling:** More comprehensive error handling and logging mechanisms.
* **Configuration Management:** Using tools like AWS CloudFormation, AWS CDK, or Terraform for Infrastructure as Code (IaC) rather than manual console setup.
* **Scalability & Performance:** Designing for scalability and performance based on expected load.
* **Testing:** Implementing unit, integration, and potentially end-to-end tests.