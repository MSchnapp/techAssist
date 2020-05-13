const mongoose = require('mongoose');

const express = require('express');

var cors = require('cors');

const bodyParser = require('body-parser');

const logger = require('morgan');

const Tools = require('./data');

const API_PORT = 3001;

const app = express();

app.use(cors());

const router = express.Router();

const dbRoute = 'mongodb+srv://mschnapp:Astech0099!@techAssist-3kix2.mongodb.net/tools?retryWrites=true&w=majority';

mongoose.connect(dbRoute, { useNewUrlParser: true, useFindAndModify: false,  useUnifiedTopology: true });

let db = mongoose.connection;

db.once('open', () => console.log('Connected to the Database'));

db.on('error', console.error.bind(console, 'MongoDB connection error: '));

app.use(bodyParser.urlencoded({ extended: false }));

app.use(bodyParser.json());

app.use(logger('dev'));

mongoose.set('useCreateIndex', true);

router.get('/getData', (req, res) => {
    Tools.find((err, tools) => {
        if(err) return res.json({ success: false, error: err });
            return res.json({ success: true, tools: tools});
    });
});

router.put('/updateScanType', (req, res) => {
    const {tool} = req.body
    Tools.findOneAndUpdate({_id: tool._id},
                           {$set: {prescan: tool.prescan,
                                   postscan: tool.postscan,
                                   roNumber: tool.roNumber}},
                                   (err, updatedTool) => {
                                     console.log(updatedTool, "Updated")
                                     console.log(tool.roNumber)
                                     if(err) {
                                       console.log("update")
                                       return res.json({success: false, error: 'Unable to update'})}
                                       return res.json({success: true})
                            })
                        })

router.put('/updateError', (req, res) => {
    const {tool} = req.body
    Tools.findOneAndUpdate({_id: tool._id},
                           {$set: {error: tool.error}},
                           (err, updatedTool) => {
                               console.log(updatedTool, 'Updated')
                               if(err) {
                                   console.log('update')
                                   return res.json({success: false, error: 'Unable to update'})}
                                   return res.json({success: true})
                           })
                        })

router.put('/updateScanCurrent', (req, res) => {
    const {tool} = req.body
    Tools.findOneAndUpdate({_id: tool._id},
                           {$set: {scancurrent: tool.scancurrent}},
                           (err, updatedTool) => {
                               console.log(updatedTool, 'Updated')
                               if(err) {
                                   console.log('update')
                                   return res.json({success: false, error: 'Unable to update'})}
                                   return res.json({success: true})
                           })
                        })

router.get('/searchTools', (req, res) => {
  const { toolSearch } = req.query  
  const query = {
      $and: [
        {toolName: {$regex: toolSearch, $options: 'i'}}
      ]
    }
    Tools.find(query, (err, results) => {
      console.log(results)
      if(err)
        return res.json({success: false, error: "Unable to perform search"}) 
        return res.json({ success: true, results: results})
    });
});

router.delete('/deleteTool', (req, res) => {
    const { _id } = req.query
    console.log(req.query, 'id!')

    Tools.deleteOne({_id}, (err, tool) => {
      if (err) return console.log(err, 'err!')
        console.log(tool, 'Tool Deleted!')
          return res.json({ success: true });
    });
    console.log("Deleted")
  });

router.post('/createTool', (req, res) => {
    let tools = new Tools();
    const { toolName, roNumber, scancurrent, errorID, prescan, postscan, paired, error } = req.body;
    if (!toolName) {
      return res.json({ success: false, error: 'Please enter tool name.'});
    }
      tools.toolName = toolName;
      tools.roNumber = roNumber;
      tools.prescan= prescan;
      tools.postscan = postscan;
      tools.error = error;
      tools.paired = paired;
      tools.scancurrent = scancurrent;
      tools.errorID = errorID;
      tools.save((err, tool) => {
          if (err) return res.json({ success: false, error: err });
            console.log("No error, saving tool successful!");
              return res.json({ success: true, data: tool})
    });
});                       

app.use('/api', router);

app.listen(API_PORT, () => console.log(`Listening on port ${API_PORT}`));