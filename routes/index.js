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
  const accountName = params.account1Name;
  const accountHolder = params.account1Holder;
  const accountNumber = params.account1Number;
  const currentBalance = Number(params.account1CurrentBalance);
  const availableBalance = Number(params.account1AvailableBalance);
  const transactionCount = Number(params.account1TransactionCount);

  console.log(typeof accountCount);

  var site = builder.create('site')
    .ele('status', 0).up();

  for(var a = 1; a <= accountCount; a++){
    var account = builder.create('bankAccount')
      .att('acctType', 'checking')
      .att('uniqueId', '21232423')
      .ele('accountName', accountName).up()
      .ele('accountNumber', accountNumber).up()
      // .ele('accountNumber', 'XXX-XXX0118').up()
      .ele('accountHolder', accountHolder).up()
      .ele('balance', {'balType':'availableBalance'})
        .ele('curAmt', {'curCode':'USD'}, availableBalance).up()
      .up()
      .ele('balance', {'balType':'currentBalance'})
        .ele('curAmt', {'curCode':'USD'}, currentBalance).up()
      .up()
      .ele('transactionList');

    for(var t = 1; t <= transactionCount; t++){
      var transaction = builder.create('transaction')
        .att('baseType', 'credit')
        .att('type', 'deposit')
        .att('uniqueId', String(t))
        .ele('description', 'SANTA CRUZ CNTY  DES:PAYROLL  ID: xx2345  INDN:JOHNSON  G R  CO ID:1946').up()
        .ele('link', 'http://www.altova.com').up()
        .ele('amount', {'curCode':'USD'}, '4995.31').up()
        .ele('transDate', {'localFormat':'yyyy-MM-dd'}, '2017-12-06T00:00:00').up()
        .ele('checkNumber', 319).up()
        .ele('category', {'categoryId':'deposit 319'}, 'other').up();
      account.importDocument(transaction);
    }
    site.importDocument(account);
  }
  // site.end({pretty: true});

  // console.log(xml);
  return(site.end({pretty: true}));
}
