# Public Exam Platform

A comprehensive platform for conducting, managing, and analyzing public examinations online.

## Project Overview

This project is designed to provide a robust and scalable solution for administering public exams. It enables exam administrators to create and manage exams, allows candidates to take exams securely, and provides detailed analytics and reporting capabilities.

## Project Structure

```
Projeto-teste/
├── docs/                      # Documentation files
│   ├── API.md                # API documentation
│   ├── SETUP.md              # Setup and installation guide
│   └── USER_GUIDE.md         # User manual
├── src/                       # Source code
│   ├── frontend/             # Frontend application
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API service calls
│   │   └── styles/           # CSS and styling
│   ├── backend/              # Backend application
│   │   ├── api/              # API endpoints and controllers
│   │   ├── models/           # Database models
│   │   ├── middleware/       # Express middleware
│   │   ├── services/         # Business logic
│   │   └── routes/           # Route definitions
│   └── database/             # Database configuration
│       ├── migrations/       # Database migrations
│       └── seeds/            # Sample data
├── tests/                     # Test files
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
├── config/                    # Configuration files
│   ├── development.env       # Development environment variables
│   ├── production.env        # Production environment variables
│   └── test.env              # Test environment variables
├── .gitignore                # Git ignore rules
├── package.json              # Project dependencies
├── README.md                 # This file
└── LICENSE                   # Project license

```

## Key Features

- **Exam Management**: Create, schedule, and manage multiple exams
- **Candidate Registration**: Secure registration and authentication system
- **Exam Taking**: Secure exam environment with question randomization and time management
- **Real-time Monitoring**: Monitor exam progress in real-time
- **Answer Evaluation**: Automatic and manual grading options
- **Analytics & Reporting**: Detailed results analysis and performance metrics
- **Security**: Role-based access control and data encryption

## Technology Stack

- **Frontend**: React.js, Redux, Axios
- **Backend**: Node.js, Express.js
- **Database**: PostgreSQL/MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: Jest, Mocha, Cypress
- **Deployment**: Docker, Docker Compose

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn package manager
- PostgreSQL/MongoDB (depending on configuration)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/johny17111/Projeto-teste.git
cd Projeto-teste
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp config/development.env .env
```

4. Run database migrations:
```bash
npm run migrate
```

5. Start the development server:
```bash
npm run dev
```

## Running Tests

```bash
# Run all tests
npm test

# Run unit tests
npm run test:unit

# Run integration tests
npm run test:integration

# Run e2e tests
npm run test:e2e
```

## API Documentation

For detailed API documentation, please refer to [docs/API.md](docs/API.md)

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions, please open an issue on the GitHub repository or contact the development team.

---

**Last Updated**: 2025-12-28
