/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
  
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {
	//return { message: 'Hello World' };
	const c_apikey = "coUgxtDGP0Uy7_tCvtZMa2vWfDA5lYWPKtlgq-0W6Rzu";
	const c_url = "https://57d360a5-45ae-43cb-a197-808795e4f84f-bluemix.cloudantnosqldb.appdomain.cloud";
	const authenticator = new IamAuthenticator({ apikey: c_apikey });
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(c_url);

    //let dbListPromise = getDbs(cloudant);
    //return dbListPromise;
    
    let allRecords = getAllRecords(cloudant, 'dealerships', params.state);
    return allRecords
}

function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
         cloudant.getAllDbs()
             .then(body => {
                 resolve({ dbs: body.result });
             })
             .catch(err => {
                  console.log(err);
                 reject({ err: err });
             });
     });
 }
 
function getAllRecords(cloudant,dbname, state) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true })            
             .then((result)=>{
                 resolve(loopResult(result.result.rows, state))
                //resolve({result:result.result.rows[0]["doc"]});
                //resolve({result:result.result.rows});
                //resolve(result);
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }
 
 function loopResult(rows, state) {
     let returnAll = false;
     if (typeof state === 'undefined')
        returnAll = true;
     
     let allRows = []
     rows.forEach((aRow)=>{ 
         if (returnAll || state === aRow["doc"]["state"])
         {
             let t = {id: aRow["doc"]["id"],
                 city: aRow["doc"]["city"],
                 state: aRow["doc"]["state"],
                 st: aRow["doc"]["st"],
                 address: aRow["doc"]["address"],
                 zip: aRow["doc"]["zip"],
                 lat: aRow["doc"]["lat"],
                 long: aRow["doc"]["long"]
             };
             allRows.push(t);
         }
     });
     return {result: allRows};
     //return {result: result.result.rows};
 }
 