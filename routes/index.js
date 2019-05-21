var express = require('express');
var router = express.Router();
var builder = require('xmlbuilder');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'DAG Generator' });
});

router.get('/xml', function(req, res) {
  var generatedXML = generateXML(req.query);
  // res.set("Content-Disposition", "attachment;filename=2accts.xml");
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

    // account = generateTransactions(account, a, params);
    generateTransactions(account, a, params);

    site.importDocument(account);
  }
  return(site.end({pretty: true}));
}


function generateTransactions(account, acctNo, params){
  const transactionCount = Number(params[`account${acctNo}TransactionCount`]);
  const recurrenceDays = Number(params[`account${acctNo}TransactionRecurrenceDays`])

  var transactions = [];

  for(var t = 1; t <= transactionCount; t++){
    const dateMethod = Number(params[`account${acctNo}Transaction${t}DateMethod`]);
    const dateValue = Number(params[`account${acctNo}Transaction${t}DateValue`]);
    const description = params[`account${acctNo}Transaction${t}Description`];
    const value = Number(params[`account${acctNo}Transaction${t}Value`]);
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

    switch(dateMethod){
      case 0: // Once
        var daysToAdd = Math.floor((Math.random() * recurrenceDays) + 1);
        var transDate = new Date();
        transDate.setDate(transDate.getDate() - daysToAdd);

        var randValue = (Math.random() * 500).toFixed(2);
        var transactionData = {
          'baseType':baseType,
          'type':type,
          'uniqueId':String(t),
          'description':generateHipsum(),
          'link':'http://www.financialapps.com',
          'curCode':params[`account${acctNo}CurrencyCode`],
          'value':value,
          // 'value':randValue,
          'transDate':transDate.toJSON(),
          'checkNumber':319,
          'category':'other'
        };

        transactions.push(transactionData);
        break;
      case 1: // Offset
        for(var f = 0; f < recurrenceDays; f += dateValue){
          var transDate = new Date();
          transDate.setDate(transDate.getDate() - f);

          var transactionData = {
            'baseType':baseType,
            'type':type,
            'uniqueId':String(t),
            'description':description,
            'link':'http://www.financialapps.com',
            'curCode':params[`account${acctNo}CurrencyCode`],
            'value':value,
            'transDate':transDate.toJSON(),
            'checkNumber':319,
            'category':'other'
          };

          transactions.push(transactionData);
        }
        break;
      case 2: // Recurring bi-weekly on day of week set in dateValue
        for(var f = 7; f < recurrenceDays; f += 14){
          var day = new Date().getDate() + (dateValue - new Date().getDay() - 1) - f;
          var transDate = new Date();
          transDate.setDate(day);

          var transactionData = {
            'baseType':baseType,
            'type':type,
            'uniqueId':String(t),
            'description':description,
            'link':'http://www.financialapps.com',
            'curCode':params[`account${acctNo}CurrencyCode`],
            'value':value,
            'transDate':transDate.toJSON(),
            'checkNumber':319,
            'category':'other'
          };

          transactions.push(transactionData);
        }
        break;
      case 3: // Recurring monthly on day of month set in dateValue
        var start = 0;
        if(new Date().getDate() < dateValue){
          start = 1;
        }

        var earliest = new Date();
        earliest.setDate(earliest.getDate() - recurrenceDays);
        var between = monthDiff(earliest, new Date());
        if(earliest.getDate() > dateValue){
          between -= 1;
        }

        for(var f = start; f <= between; f++){
          var transDate = new Date();
          transDate.setMonth(transDate.getMonth() - f)
          transDate.setDate(dateValue);

          var transactionData = {
            'baseType':baseType,
            'type':type,
            'uniqueId':String(t),
            'description':description,
            'link':'http://www.financialapps.com',
            'curCode':params[`account${acctNo}CurrencyCode`],
            'value':value,
            'transDate':transDate.toJSON(),
            'checkNumber':319,
            'category':'other'
          };
          transactions.push(transactionData);
        }
        break;
      case 4: // Random transactions across recurrence days coming to average amount weekly
        var totalTrans = 0
        var totalAmount = 0
        for(var f = 7; f < recurrenceDays; f += 7){
          totalTrans += 1;
          var transactionAmounts = [];
          while (transactionAmounts.reduce(getSum, 0) < (value - 30)){
            transactionAmounts.push(Number((Math.random() * (value / 7)).toFixed(2)))
          }
          console.log(transactionAmounts.length);
          console.log(transactionAmounts.reduce(getSum, 0));
          totalAmount += transactionAmounts.reduce(getSum, 0);
          for (var l = 0; l < transactionAmounts.length; l++){
            var day = new Date().getDate() + ((Math.random() * 7) - new Date().getDay() - 1) - f;
            var transDate = new Date();
            transDate.setDate(day);
            // var transDate = new Date();
            // transDate.setDate(transDate.getDate() - f);

            var transactionData = {
              'baseType':baseType,
              'type':type,
              'uniqueId':String(t),
              'description':generateSimpleDesc(),
              'link':'http://www.financialapps.com',
              'curCode':params[`account${acctNo}CurrencyCode`],
              'value':transactionAmounts[l],
              'transDate':transDate.toJSON(),
              'checkNumber':319,
              'category':'other'
            };

            transactions.push(transactionData);
          }
        }
        console.log(`Average: ${totalAmount / totalTrans}`);
        break;
      case 5: // Recurring monthly amount range
        var start = 0;
        if(new Date().getDate() < dateValue){
          start = 1;
        }

        var earliest = new Date();
        earliest.setDate(earliest.getDate() - recurrenceDays);
        var between = monthDiff(earliest, new Date());
        if(earliest.getDate() > dateValue){
          between -= 1;
        }

        for(var f = start; f <= between; f++){
          var transDate = new Date();
          transDate.setMonth(transDate.getMonth() - f);
          transDate.setDate(dateValue);

          var transValue = (Math.random() * ((value + 31) - value) + value).toFixed(2);

          var transactionData = {
            'baseType':baseType,
            'type':type,
            'uniqueId':String(t),
            'description':description,
            'link':'http://www.financialapps.com',
            'curCode':params[`account${acctNo}CurrencyCode`],
            'value':transValue,
            'transDate':transDate.toJSON(),
            'checkNumber':319,
            'category':'other'
          };
          transactions.push(transactionData);
        }
        break;
    }
  }
  transactions.sort(function(a, b) {
    return new Date(a.transDate) - new Date(b.transDate);
  });

  for(var d in transactions){
    var transaction = builder.create('transaction')
      .att('baseType', transactions[d].baseType)
      .att('type', transactions[d].type)
      .att('uniqueId', Number(d) + 1)
      .ele('description', transactions[d].description).up()
      // .ele('link', transactions[d].link).up()
      .ele('amount', {'curCode':transactions[d].curCode}, Number(transactions[d].value).toFixed(2)).up()
      .ele('transDate', {'localFormat':'yyyy-MM-dd'}, transactions[d].transDate).up()
      .ele('checkNumber', transactions[d].checkNumber).up()
      .ele('category', transactions[d].category).up();

    account.importDocument(transaction);
  }
}

function monthDiff(d1, d2) {
    var months;
    months = (d2.getFullYear() - d1.getFullYear()) * 12;
    months -= d1.getMonth();
    months += d2.getMonth();
    return months <= 0 ? 0 : months;
}

function generateHipsum(){
  var hipsum = ["Beard", "sriracha", "migas", "synth", "franzen", "health", "goth", "authentic", "craft", "beer", "chambray", "neutra", "meh", "snackwave", "cred", "Tote", "bag", "venmo", "man",
  "bun", "lomo", "pok", "pok", "mixtape", "forage", "hot", "chicken", "palo", "santo", "kale", "chips", "retro", "humblebrag", "Roof", "party", "ugh", "quinoa", "forage", "locavore",
  "drinking", "vinegar", "Food", "truck", "shoreditch", "lomo", "pickled", "live-edge", "brunch", "skateboard", "cornhole", "enamel", "pin", "adaptogen", "tote", "bag", "fanny", "pack", "Deep", "v",
  "tilde", "heirloom", "cronut", "artisan", "man", "braid", "irony", "pinterest"];

  var hipsumDesc = "";
  for (var h = 0; h < Math.floor((Math.random() * 5) + 2); h++){
    hipsumDesc += `${hipsum[Math.floor(Math.random() * hipsum.length)]} `;
  }
  return hipsumDesc
}

function generateSimpleDesc(){
  var letters = ["A", "B", "C", "D", "E", "F"];
  return `Transaction ${letters[Math.floor(Math.random() * letters.length)]}`;
}

function getSum(total, num) {
  return total + num;
}
