# Calendar App


A desktop application that automates the creation of calendar events for important company deadlines using Microsoft Entra ID (formerly Azure AD) and Companies House API. Built with Python, Flask, and Microsoft Graph API, the app allows users to manage and stay up-to-date with company compliance deadlines by integrating deadlines directly into a Microsoft calendar.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [License](#license)

## Features

- **Microsoft Entra ID Authentication**: Secure login and calendar access using Microsoft Entra ID.
- **Automated Calendar Events**: Extracts and creates calendar events for company deadlines like account filing and confirmation statements.
- **Company Information Retrieval**: Fetches company details and deadlines via Companies House API.

## Technologies Used

- **Python**: Backend logic and API handling
- **Flask**: Lightweight server for handling API calls
- **Microsoft Graph API**: Integrates calendar event creation into a Microsoft calendar
- **Companies House API**: Retrieves company deadlines and compliance dates

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/company-deadline-manager.git
   cd company-deadline-manager
