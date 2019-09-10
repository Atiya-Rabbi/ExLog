var Xray = require('x-ray');
var x = Xray();
var express = require('express')
var app = express()
app.use(function(req, res,next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next()
});
app.get('/', function (req, res){
//console.log(req.query.url)
  url = req.query.url
  //console.log("this is parameter",url)
   x(url,{title:'title',image:'meta[property="og:image"]@content',desc:'meta[property="og:description"]@content',url:'meta[property="og:url"]@content',site:'meta[property="og:site_name"]@content'})(function(err, obj) {
                  if(obj.desc != undefined){
                    if(obj.desc.length>160){
                      obj.desc = obj.desc.slice(0,160)
                    }
                   }
                  if (!obj.image){
                      if (!obj.site && !obj.desc){
                        var html="<div class='card' style=' width:402px;'>" + "<a target='_blank' href=" + obj.url + ">" + "<div class='imgcon'>" +"<img id='articleimg' style='border:1x solid grey; width:400px; heigth:225px;'src=" + "'http://www.sacatonschools.org/GalleryImages/20171127155631728_image.png'" + ">" + "</div>" +"<div class='textcard' style='background-color:white; border:1px solid grey; width:400px;'>" + "<h5 style='color:black; margin-bottom: 0px; font-size:medium;margin-left:2px;'>"+ "<b>" + obj.title + "</b>" +"</h5>" +  "</div>" + "</a>" + "</div>"
                      res.send(html)
                      }
                      var html="<div class='card' style=' width:402px;'>" + "<a target='_blank' href=" + obj.url + ">" + "<div class='imgcon'>" +"<img id='articleimg' style='border:1x solid grey; width:400px; heigth:225px;'src=" + "'http://www.sacatonschools.org/GalleryImages/20171127155631728_image.png'" + ">" + "</div>" +"<div class='textcard' style='background-color:white; border:1px solid grey; width:400px;'>"+ "<h6 style='font-style: oblique; margin-top: 2px; margin-left: 2px; font-size: small; color: slategrey; margin-bottom: 0px;'>" +obj.site+ "</h6>" + "<h5 style='color:black; margin-bottom: 0px; font-size:medium;margin-left:2px;'>"+ "<b>" + obj.title + "</b>" +"</h5>" + "<p style='color: slategray; margin-bottom: 0px; margin-top:1px; font-size: small;margin-left:2px;'>"+obj.desc + "</p>" + "</div>" + "</a>" + "</div>"
                      res.send(html)
rl
                  }
                  else if(!obj.desc){
                  var html="<div class='card' style=' width:402px;'>" + "<a target='_blank' href=" + obj.url + ">" +"<div class='imgcon'>"+ "<img id='articleimg' style='border:1x solid grey; width:400px; heigth:225px;'src=" + obj.image + ">" + "</div>" + "<div class='textcard' style='background-color:white; border:1px solid grey; width:400px;'>"+ "<h6 style='font-style: oblique;color: slategrey; margin-bottom: 0px; margin-top: 2px; margin-left: 2px; font-size: small;'>" +obj.site+ "</h6>" + "<h5 style='color:black;margin-bottom: 0px; font-size:medium;margin-left:2px;'>"+ "<b>" + obj.title + "</b>" +"</h5>" + "</div>" + "</a>" + "</div>"
                  res.send(html)
                  }
                  else if(!obj.site){
                    var html="<div  class='card' style=' width:402px;'>" + "<a target='_blank' href=" + obj.url + ">" +"<div class='imgcon'>"+ "<img id='articleimg' style='border:1x solid grey; width:400px; heigth:225px;'src=" + obj.image + ">" + "</div>" + "<div class='textcard' style='background-color:white; border:1px solid grey; width:400px;'>" + "<h5 style='color:black; margin-bottom: 0px; font-size:medium;margin-left:2px;'>"+ "<b>" + obj.title + "</b>" +"</h5>" + "<p style='color: slategray; margin-bottom: 0px; margin-top:1px; font-size: small;margin-left:2px;'>"+obj.desc + "</p>" + "</div>" + "</a>" + "</div>"
                      res.send(html)
                  }

                    else{
                      if(obj.image == "/img/misc/og-default.png"){
                        var html="<div  class='card' style=' width:402px;'>" + "<a target='_blank' href=" + obj.url + ">" + "<div class='imgcon'>" +"<img id='articleimg' style='border:1x solid grey; width:400px; heigth:225px;'src="+ "'http://static1.squarespace.com/static/560e9561e4b0631d94aec1e1/560eb44ce4b04465aea865e3/56e829ceb654f9ada96ade9c/1458055804193/hello+gig+logo.jpeg?format=1000w'" + ">"+ "</div>" + "<div class='textcard' style='background-color:white; border:1px solid grey; width:400px;'>" +"<h6 style='font-style: oblique;color: slategrey; margin-bottom: 0px; margin-top: 2px; margin-left: 2px; font-size: small;'>" + obj.site + "</h6>" + "<h5 style='color:black; margin-bottom: 0px; font-size:medium;margin-left:2px;'>"+ "<b>" + obj.title + "</b>" +"</h5>" + "<p style='color: slategray; margin-bottom: 0px; margin-top:1px; font-size: small;margin-left:2px;'>" + obj.desc + "</p>" + "</div>" + "</a>" + "</div>"
                       res.send(html)
                      }
                        var html="<div  class='card' style=' width:402px;'>" + "<a target='_blank' href=" + obj.url + ">" + "<div class='imgcon'>" + "<img id='articleimg' style='border:1x solid grey; width:400px;'src=" + obj.image + ">" +"</div>"+ "<div class='textcard' style='background-color:white; border:1px solid grey; width:400px;'>"+ "<h6 style='font-style: oblique; margin-top: 2px; margin-left: 2px; font-size: small; color: slategrey; margin-bottom: 0px;'>" +obj.site+ "</h6>" + "<h5 style='color:black; margin-bottom: 0px; font-size:medium;margin-left:2px;'>"+ "<b>" + obj.title + "</b>" +"</h5>" + "<p style='color: slategray; margin-bottom: 0px; margin-top:1px; font-size: small;margin-left:2px;'>" + obj.desc + "</p>" + "</div>" + "</a>" + "</div>"
                       res.send(html)

                    }

    })
})
app.listen(8081)
