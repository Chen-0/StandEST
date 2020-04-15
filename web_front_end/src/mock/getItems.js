let demoList = [{
  _id: "xxxx",
  name: "合生元奶粉一段100g",
  no: "12345678911"
},{
  _id: "xxxx",
  name: "合生元奶粉一段200g",
  no: "12345678912"
},{
  _id: "xxxx",
  name: "合生元奶粉一段300g",
  no: "12345678913"
},{
  _id: "xxxx",
  name: "合生元奶粉一段800g",
  no: "1234567890"
},{
  _id: "xxxx",
  name: "合生元奶粉一段800g",
  no: "1234567890"
},{
  _id: "xxxx",
  name: "合生元奶粉一段800g",
  no: "1234567890"
},]

export default {
'get|/getItems':  option => {
return {
status: 200,
message: 'success',
data: demoList
};
}
}