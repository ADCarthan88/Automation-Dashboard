const { Stack, Duration } = require('aws-cdk-lib');
const lambda = require('aws-cdk-lib/aws-lambda');
const apigateway = require('aws-cdk-lib/aws-apigateway');
const dynamodb = require('aws-cdk-lib/aws-dynamodb');

class AutomationStack extends Stack {
  constructor(scope, id, props) {
    super(scope, id, props);

    const tasksTable = new dynamodb.Table(this, 'TasksTable', {
      tableName: 'automation-tasks',
      partitionKey: { name: 'taskId', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    const emailParserFunction = new lambda.Function(this, 'EmailParserFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'lambda_function.lambda_handler',
      code: lambda.Code.fromAsset('../lambda-functions/email-parser'),
      timeout: Duration.seconds(30),
    });

    const invoiceGeneratorFunction = new lambda.Function(this, 'InvoiceGeneratorFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'lambda_function.lambda_handler',
      code: lambda.Code.fromAsset('../lambda-functions/invoice-generator'),
      timeout: Duration.seconds(30),
    });

    const leadScorerFunction = new lambda.Function(this, 'LeadScorerFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'lambda_function.lambda_handler',
      code: lambda.Code.fromAsset('../lambda-functions/lead-scorer'),
      timeout: Duration.seconds(30),
    });

    tasksTable.grantReadWriteData(emailParserFunction);
    tasksTable.grantReadWriteData(invoiceGeneratorFunction);
    tasksTable.grantReadWriteData(leadScorerFunction);

    const api = new apigateway.RestApi(this, 'AutomationApi', {
      restApiName: 'Automation Dashboard API',
      description: 'API for automation dashboard',
    });

    const emailIntegration = new apigateway.LambdaIntegration(emailParserFunction);
    const invoiceIntegration = new apigateway.LambdaIntegration(invoiceGeneratorFunction);
    const leadIntegration = new apigateway.LambdaIntegration(leadScorerFunction);

    const emailResource = api.root.addResource('email-parse');
    emailResource.addMethod('POST', emailIntegration);

    const invoiceResource = api.root.addResource('invoice-generate');
    invoiceResource.addMethod('POST', invoiceIntegration);

    const leadResource = api.root.addResource('lead-score');
    leadResource.addMethod('POST', leadIntegration);
  }
}

module.exports = { AutomationStack };