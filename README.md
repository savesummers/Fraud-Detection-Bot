# 🛡️ Fraud Detection Bot for Financial Transactions

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## **Project Overview**  
This Python project analyzes client bank transactions to automatically identify **red flags** indicating potential fraudulent or high-risk activities. It uses **rule-based checks**, **threshold calculations**, and optional **web scraping** to detect suspicious transactions.

---

## **Features**  
- 💰 **Large Transaction Detection:** Flags transactions ≥ $10,000.  
- 🌍 **High-Risk Country Detection:** Detects transactions involving TAFT high-risk countries or sanctioned countries (e.g., OFAC list).  
- 🏦 **Cash-Intensive / High-Risk Sector Detection:** Identifies transactions related to casinos, gambling, real estate, precious metals, jewelry, crypto exchanges, NGOs, charities, or Money Service Businesses (MSBs).  
- 📊 **Cumulative Cash Calculation:** Flags if total cash transactions exceed $10,000.  
- 🗓️ **Transaction Frequency Monitoring:** Detects months with unusually high transaction frequency (≥ 3 per week).  
- ✅ **Boolean Flagging:** Outputs True/False indicators for threshold conditions.  
- 📝 **Automated Reporting:** Generates a structured text report summarizing all red flags.  

---

## **Getting Started**

### **Requirements**
- Python 3.x  
- Required Python packages:
```bash
pip install pandas serpapi
