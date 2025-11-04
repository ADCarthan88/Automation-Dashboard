module.exports = {
  aws: {
    region: 'us-east-1',
    lambdaFunctions: {
      emailParser: 'email-parser',
      invoiceGenerator: 'invoice-generator',
      leadScorer: 'lead-scorer'
    }
  },
  api: {
    baseUrl: process.env.API_BASE_URL || 'http://localhost:8000',
    timeout: 30000
  },
  database: {
    dynamoTablePrefix: 'automation-dashboard'
  }
};