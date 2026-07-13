const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const html = fs.readFileSync('marg_pharma.html', 'utf8');

const dom = new JSDOM(html, { runScripts: "dangerously" });
const window = dom.window;

// Setup globals
window.G = { items: [] };
window.g = function(id) { 
  if (id === 'am-id') return {value: ''};
  if (id === 'am-nm') return {value: 'PANADOL'};
  if (id === 'am-sl') return {value: 'PARA'};
  if (id === 'am-co') return {value: 'GSK'};
  if (id === 'am-pk') return {value: '10x10'};
  if (id === 'am-rt') return {value: '10'};
  if (id === 'med-list') return window.document.createElement('div');
  return null;
};
window.cm = function() {};
window.sv = function() {};
window.API_BASE = '';

// intercept alert and confirm
window.alert = console.log;
window.confirm = () => true;
window.fetch = () => Promise.resolve({ json: () => Promise.resolve({success: true}) });

// run the saveMed
window.saveMed();
console.log("After save:", window.G.items);

// run renderMedList
let fakeDiv = window.document.createElement('div');
fakeDiv.id = 'med-list';
window.document.body.appendChild(fakeDiv);
window.g = function(id) { 
  if(id === 'med-list') return fakeDiv; return {value:''};
};
window.renderMedList();

console.log("innerHTML:", fakeDiv.innerHTML);

// extract id
let addedId = window.G.items[0].id;
window.deleteMed(addedId);
console.log("After delete:", window.G.items);

