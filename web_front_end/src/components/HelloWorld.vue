<template>
  <div class="container-fluid rc-main">
    <div class="left-cc no-select">
      <div :class="{'item': true, 'active': isActive(item)}" v-for="(item, index) in items" :key="index">
        <input :id="'kkkk' + index" type="checkbox" @change="handleClick(item)" />
        <label :for="'kkkk' + index">
          <span></span>
          {{ item.item_name }}
          <ins>
            <i>{{ item.item_name }}</i>
          </ins>
        </label>
      </div>
    </div>
    <div class="right-cc">
      <div class="btn-group">
        <div class="submit-btn" v-on:click="handleFormPost()">开始计算</div>
        <!-- <div class="reset-btn" v-on:click="handleFormPost()">重置</div> -->
      </div>

      <table  class="blueTable">
        <tr>
          <th>商品名称</th>
          <th>得分</th>
        </tr>
        <tr :key="index" v-for="(item, index) in resultList">
          <td>{{item.item_name}}</td>
          <td>{{item.score}}</td>
        </tr>
      </table>


    </div>
  </div>
</template>

            // <div
            //   v-on:click="handleClick(item)"
            //   :class="{'vbtn': true, 'active': isActive(item)}"
            // ></div>

<script>
import axios from "axios";
import _ from "lodash";
import qs from "Qs";

export default {
  name: "HelloWorld",
  data() {
    return {
      items: [],
      selectList: [],
      resultList: []
    };
  },
  created() {
    axios.get("/api/getItems").then(res => {
      this.items = res.data;

      console.log(this.items);
    });
  },
  methods: {
    handleClick(row) {
      if (!_.includes(this.selectList, row.item_no)) {
        this.selectList = _.concat(this.selectList, row.item_no);
      } else {
        const xt = _.remove(this.selectList, function(n) {
          return n != row.item_no;
        });
        this.selectList = xt;
      }
    },
    isActive(item) {
      return _.includes(this.selectList, item.item_no);
    },
    handleReset() {

    },
    handleFormPost() {
      if (this.selectList.length <= 1) {
        alert("请选择更多商品");
        return;
      }

      axios
        .post(
          "/api/estGoods",
          qs.stringify({
            items: JSON.stringify(this.selectList)
          })
        )
        .then(res => {
          let items = res.data;
          console.log(items);

          this.resultList = items;
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import "./style.scss";
</style>
