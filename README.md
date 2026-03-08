# Post-Deployment Microservice CPU Risk Prediction

## Project Overview
Modern cloud applications rely heavily on microservices, which are frequently updated and deployed. However, performance issues such as CPU spikes or gradual slowdowns may appear **after deployment**, potentially leading to service instability or failure.

This project develops a **machine learning–based risk prediction system** that analyzes CPU telemetry data and predicts potential CPU-related risks before they escalate into critical failures.

The system combines **statistical analysis, machine learning, and interactive visualizations** to support proactive monitoring and decision-making.

---

## Problem Statement
Traditional monitoring tools detect issues **only after they occur**. In many real-world datasets, **actual failure labels are not available**, making it difficult to train standard supervised models.

This project addresses the problem by:
- Defining **risk conditions using statistical thresholds**
- Predicting **CPU risk probability using machine learning**
- Providing **early warning insights through dashboards**

---

## Project Objectives
- Analyze CPU usage patterns in microservices after deployment
- Detect abnormal CPU behavior using statistical thresholds
- Predict potential CPU risk using machine learning
- Provide early warning insights through visualization dashboards
- Help DevOps teams monitor system health and prevent downtime

---

## Methodology

### Data Analysis
The system analyzes key telemetry metrics such as:

- CPU Usage
- CPU Variability (Rolling Standard Deviation)

These indicators help identify **unstable system behavior**.

---

### Risk Definition
Since real failure labels were not available, risk was defined using **statistical thresholds**.

A **70th percentile threshold** was used to identify abnormal CPU conditions.

When CPU usage and variability cross this threshold, the instance is classified as **high-risk**.

---

### Machine Learning Model
A **Logistic Regression model** was used to predict CPU risk probability.

Output:
- Risk probability between **0 and 1**

Example:

| Probability | Risk Level |
|-------------|------------|
| 0.20 | Low Risk |
| 0.75 | High Risk |

---

### Risk Score
The predicted probability is converted into a **Risk Score (0–100%)** to make interpretation easier.

Example:

| Probability | Risk Score |
|-------------|------------|
| 0.45 | 45% |
| 0.82 | 82% |

---

### Hours-to-Failure Estimation
The system estimates how soon a failure might occur.

Steps:
1. Identify when the **risk score reaches the high-risk threshold**
2. Compare with the **current timestamp**
3. Calculate the **estimated hours to failure**

This provides **early warning signals** for engineers.

---

## Visualization

### Streamlit Dashboard
An interactive **Streamlit application** was developed to visualize:

- CPU usage trends
- Risk score progression
- System health indicators
- Early risk alerts

### Tableau Dashboard
A **Tableau dashboard** provides deeper analytics including:

- CPU usage trends
- Risk score trends
- Deployment performance insights
- System monitoring indicators

These dashboards help teams **visually monitor system behavior and risk levels**.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Tableau
- Machine Learning

---

## Project Workflow

1. Data collection and preprocessing
2. CPU behavior analysis
3. Risk definition using statistical thresholds
4. Logistic Regression model training
5. Risk score calculation
6. Hours-to-failure estimation
7. Visualization using Streamlit and Tableau

---

## Key Benefits

- Early detection of performance degradation
- Predictive insights for system monitoring
- Support for DevOps performance analysis
- Reduced risk of unexpected microservice downtime

---

## Important Note
This system is designed as a **decision-support tool**. It should be used alongside traditional monitoring systems rather than replacing them.

---

## Author
Developed as part of a **Data Analytics / Machine Learning project** focused on predictive monitoring of microservices.
