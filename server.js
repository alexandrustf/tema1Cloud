const http = require("http");
const https = require("https");
const { parse } = require("querystring");
const { exec } = require("child_process");
const url = require("url");
var sleep = require("sleep");
toBePrinted = "";
const server = http.createServer((req, res) => {
  const reqUrl = url.parse(req.url, true);
  console.log(reqUrl.pathname);
  console.log(req.method);

  if (reqUrl.pathname == "/api" && req.method === "GET") {
    console.log("Request Type:" + req.method + " Endpoint: " + reqUrl.pathname);
    exec(
      `py "..\\..\\Practica in Python\\Tema1Cloud\\main.py" ${reqUrl.query.name}`,
      (error, stdout, stderr) => {
        if (error) {
          console.log(`error: ${error.message}`);
          return;
        }
        if (stderr) {
          console.log(`stderr: ${stderr}`);
          return;
        }
        console.log(`Your search info: ${stdout}`);
        sleep.sleep(15);
        toBePrinted = stdout;
      }
    );
    response = toBePrinted;
    res.statusCode = 200;
    res.setHeader("Content-Type", "application/json");
    res.end(toBePrinted);
  }
  console.log(req.url);
  if (req.method === "POST") {
    collectRequestData(req, result => {
      console.log(result);
      res.write(`            
                <!doctype html>
                <html>
                <body>
                <h1>Your hero name is ${result.fname} </h1><br><br>`);
      console.log(
        `py "..\\..\\Practica in Python\\Tema1Cloud\\main.py" ${result.fname}`
      );
      exec(
        `py "..\\..\\Practica in Python\\Tema1Cloud\\main.py" ${result.fname}`,
        (error, stdout, stderr) => {
          if (error) {
            console.log(`error: ${error.message}`);
            return;
          }
          if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
          }
          console.log(`Your search info: ${stdout}`);
          toBePrinted = stdout;
        }
      );
      res.write(`<br>stdout: ${toBePrinted}`);
      res.write(
        `<br><br><a href=".">
                    <button>Go Back!</button>
                </a>        
                </body>
                </html>`
      );
      res.end();
    });
  } else {
    res.end(`
        <!doctype html>
        <html>
        <body>
            <h1>Enter your favourite HERO from Star Wars!</h1><br><br>
            <form action="/" method="post">
                <input type="text" name="fname" /><br />
                <button>Save</button>
            </form>

        </body>
        </html>
      `);
  }
});
server.listen(8085);
// function getResponse(name){
//     return callToApi();
// }
// function callToApi(){
//     returnval = ''
//     https.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY', (resp) => {
//     let data = '';

//     // A chunk of data has been recieved.
//     resp.on('data', (chunk) => {
//         data += chunk;
//     });

//     // The whole response has been received. Print out the result.
//     resp.on('end', () => {
//         console.log(JSON.parse(data).explanation);
//         returnval = JSON.parse(data).explanation;
//         datas = JSON.parse(data).explanation;
//         return JSON.stringify(data);
//     });

//     }).on("error", (err) => {
//     console.log("Error: " + err.message);
//     });
//     console.log('sunt aici')
//     console.log(returnval);
//     return 'sunt aici';
// }
function collectRequestData(request, callback) {
  const FORM_URLENCODED = "application/x-www-form-urlencoded";
  if (request.headers["content-type"] === FORM_URLENCODED) {
    let body = "";
    request.on("data", chunk => {
      body += chunk.toString();
    });
    request.on("end", () => {
      callback(parse(body));
    });
  } else {
    callback(null);
  }
}
