<template lang="jade">
  .order
    el-form.orderlist
      .order__info__title 订单详情
      .order__info-container(v-for="order in orderlist")
        el-form-item.order__info__id 订单号：NO.{{ order.id }}
        el-form-item.order__info
          .order__info__text 电影：
          .order__info__data {{ order.movieName }}
          .order__info__text 语言：
          .order__info__data {{ order.language }}
          .order__info__text 时间：
          .order__info__data {{ order.showDate}} {{ order.showTime}}
          br
          .order__info__text 场次：
          .order__info__data {{ order.room }}
          .order__info__text 票数：
          .order__info__data {{ order.seat.length }} 张
          .order__info__text 座位：
          .order__info__data(v-for="seat in order.seat")
            {{ seat.row }}行{{ seat.col }}列

</template>

<script>

import { User, Screen } from '@/models/index.js'

export default {
  name: 'hello',
  data () {
    return {
      orderlist: []
    }
  },
  created () {
    User.getOrders().then(data => {
      var list = data.filmOrderModelList.reverse()
      var promises = list.map(orderdata => {
        return new Promise(resolve => {
          Screen.getScreenById(orderdata.screenId).then(screendata => {
            let order = {}
            order.id = orderdata.id
            order.showDate = screendata.showDate
            order.showTime = screendata.showTime
            order.language = screendata.language
            order.room = screendata.room
            order.movieName = screendata.movieName
            let seat = []
            for (let row = 0; row < 8; row++) {
              for (let col = 0; col < 11; col++) {
                if (orderdata.seat[row * 11 + col] === '2') {
                  seat.push({
                    row: row + 1,
                    col: col + 1
                  })
                }
              }
            }
            order.seat = seat
            resolve(order)
          })
        })
      })
      Promise.all(promises).then(posts => {
        this.orderlist = posts
      })
    })
  },
  methods: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .orderlist {
    width: 60%;
    margin: 200px auto 100px auto;
    border: 1px solid #efefef;
    border-radius: 2px;
    box-shadow: 0px 0px 2px #d1dbe5;
  }

  .order__info-container {
    border: 1px solid #efefef;
    height: 150px;
    width: 85%;
    margin: 50px auto 50px auto;
    text-align: left;
    box-shadow: 0px 0px 4px #d1dbe5;
  }
  .order__info {
    padding-left:30px;
    height: 25px;
    width: 100%;
  }
  .order__info__title {
    width: 120px;
    height: 40px;
    line-height: 1.9;
    font-size: 24px;
    font-weight: 700;
    border-radius: 2px;
    text-align: center;
    background: #55B7FF;
    color: #fff;
    position: absolute;
    top: 160px;
  }

  .order__info__id {
    padding-left: 20px;
    font-weight: 500;
    background: #efefef;
  }
  .order__info__text {
    display: inline-block;
    text-align: left;
    font-size: 15px;
    font-weight: 500;
  }
  .order__info__data {
    display: inline-block;
    text-align: left;
    font-size: 15px;
    margin-right: 20px;
  }
</style>
