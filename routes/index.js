var express = require('express');
var router = express.Router();
var builder = require('xmlbuilder');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'DAG Generator' });
});

router.get('/xml', function(req, res) {
  var generatedXML = generateXML(req.query);
  // res.set("Content-Disposition", "attachment;filename=fantasticxmldata.xml");
  res.set("Content-Disposition", "inline;filename=fantasticxmldata.xml");
  res.set("Content-Type", "application/xml");
  res.send(generatedXML);
})

module.exports = router;


function generateXML(params){
  const accountCount = Number(params.accountCount);

  var site = builder.create('site')
    .ele('status', 0).up();

  for(var a = 1; a <= accountCount; a++){
    const containerType = params[`account${a}ContainerType`];
    const accountType = params[`account${a}AccountType`];
    const currencyCode = params[`account${a}CurrencyCode`];
    const accountName = params[`account${a}Name`];
    const accountHolder = params[`account${a}Holder`];
    const accountNumber = params[`account${a}Number`];
    const currentBalance = Number(params[`account${a}CurrentBalance`]);
    const availableBalance = Number(params[`account${a}AvailableBalance`]);

    var account = builder.create(`${containerType}Account`)
      .att('acctType', accountType)
      .att('uniqueId', a)
      .ele('accountName', accountName).up()
      .ele('accountNumber', accountNumber).up()
      .ele('accountHolder', accountHolder).up()
      .ele('balance', {'balType':'availableBalance'})
        .ele('curAmt', {'curCode':currencyCode}, availableBalance).up()
      .up()
      .ele('balance', {'balType':'currentBalance'})
        .ele('curAmt', {'curCode':currencyCode}, currentBalance).up()
      .up()
      .ele('transactionList');

    account = generateTransactions(account, a, params);

    site.importDocument(account);
  }
  // site.end({pretty: true});

  // console.log(xml);
  return(site.end({pretty: true}));
}


function generateTransactions(account, acctNo, params){
  const transactionCount = Number(params[`account${acctNo}TransactionCount`]);
  const recurrenceDays = Number(params[`account${acctNo}TransactionRecurrenceDays`])

  for(var t = 1; t <= transactionCount; t++){
    const dateMethod = params[`account${acctNo}Transaction${t}DateMethod`];
    const dateValue = params[`account${acctNo}Transaction${t}DateValue`];
    const description = params[`account${acctNo}Transaction${t}Description`];
    const value = params[`account${acctNo}Transaction${t}Value`];
    const baseType = params[`account${acctNo}Transaction${t}Type`];
    var type = "";
    switch(baseType){
      case "debit":
      type = "debit";
      break;
      case "credit":
      type = "deposit";
      break;
    };

    var transaction = builder.create('transaction')
      .att('baseType', baseType)
      .att('type', type)
      .att('uniqueId', String(t))
      .ele('description', description).up()
      .ele('link', 'http://www.altova.com').up()
      .ele('amount', {'curCode':'USD'}, value).up()
      .ele('transDate', {'localFormat':'yyyy-MM-dd'}, '2017-12-06T00:00:00').up()
      .ele('checkNumber', 319).up()
      .ele('category', 'other').up();
      // .end({pretty: true})

    account.importDocument(transaction);
    // console.log(transactions);
  }
  return(account);
}
