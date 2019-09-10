var deasync = require('deasync');
var cp = require('child_process');
var exec = deasync(cp.exec);
var express = require('express')
var app = express()
var Xray = require('x-ray');
var x = Xray();
var scrappy = require('@mrharel/scrappy');
var request = require('request');




app.get('/:session', function (req, res){
    console.log("i m")
    var session = req.params.session
    console.log(session)
    let condition;
    let article = [];
    let urlLength=0

    url="http://localhost:5000/url/" + session
    console.log(url);

    request.get(url, { json:true }, function (error, response,body){
        console.log("i m here");
       var urls = response.body
       console.log(urls)

        for(var i=0;i<urls.length;i++){
          console.log("im in loop and inviting fault")
          if (urls[i] == 'https://www.livescience.com/news'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['h2 a@href']
          }
          else if (urls[i] == 'https://edition.cnn.com/specials/politics/world-politics'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['div .media a@href']
          }
          else if (urls[i] == 'https://www.wired.co.uk/topic/business'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['article a@href']
          }
          else if (urls[i] == 'https://hbswk.hbs.edu/Pages/browse.aspx?HBSTopic=Entrepreneurship'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['h4 a@href']
          }
          else if (urls[i] == 'https://www.wired.co.uk/topic/technology'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['article a@href']
          }
          else if (urls[i] == 'https://hellogiggles.com/reviews-coverage'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['article a@href']
          }
          else if (urls[i] == 'https://hellogiggles.com/fashion'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['article a@href']
          }
          else if (urls[i] == 'https://www.everywritersresource.com/on-writing'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['div .entry-content a@href']
          }
          else if (urls[i] == 'https://www.pickthebrain.com/blog/self-improvement-articles'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['.entry-content a@href']
          }
          else if (urls[i] == 'https://www.ideafit.com/fitness-library'){
            console.log(" i m in ")
            var medium = "false";
            condition = ['h3 a@href']
          }
         console.log("extarcting is going to start")
          x(urls[i], 'body', condition)(function(err, url) {
             console.log("under extracting")
            url = url.filter( onlyUnique );
            if (url.length>30){
               url = url.slice(0,30)

            }
            console.log("I'm line 73 and len",url.length)
            urlLength +=url.length
            for(var i=0;i<url.length;i++){
                article.push(url[i])
                if(article.length == urlLength){
                       medium = "true";
                   }
                }
          })

          while(medium != "true"){
            require('deasync').runLoopOnce();
          }
    }
    if(article.length%2==0){
        res.send(article)
        article = []
    }
    else{
        article.push("https://thelady25.com/the-lady25/")

        res.send(article)
        article = []
    }


    function onlyUnique(value, index, self) {
        return self.indexOf(value) === index;
      }

     })


})
console.log("im calling 8082")
app.listen(8082)

