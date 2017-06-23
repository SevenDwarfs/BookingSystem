<template lang="jade">
  .booking
    .film
      .film__img-container
        img.film__img-container__img(:src="film.url")
      .film__content
        .film__content__title {{ film.chineseName }}
        .film__content__subtitle {{ film.englishName }}
        .film__content__info {{ film.type }}
        .film__content__info {{ film.length }}
        .film__content__info {{ film.releaseDate }} {{ film.showPlace }}
    el-steps.booking__steps(space="40%", :active="currentStep", finish-status="success", :center="true", :align-center="true")
      el-step(title="步骤 1", description="选择时间 / 地点 / 影院")
      el-step(title="步骤 2", description="选择座位")
      el-step(title="步骤 3", description="确认订单")
    el-tabs.booking-form(v-show="currentStep === 0", type="border-card")
      el-tab-pane
        span(slot="label")
          i.el-icon-date
          |  时间 / 地点 / 影院
      .slector-container
        .slecter
          .slecter__info
            img.slecter__info__icon(src="../assets/images/time.png")
            span 日期 ：
          .slecter__items
            .slecter__items__item(v-for="(time, index) in times", :class="index === timeSelect ? 'slecter__items__item--selected' : ''" , @click="changeTime(index)") {{ time }}
        .slecter
          .slecter__info
            img.slecter__info__icon(src="../assets/images/loc.png")
            span 地点 ：
          .slecter__items
            .slecter__items__item(v-for="(area, index) in areas", :class="index === areaSelect ? 'slecter__items__item--selected' : ''", @click="changeArea(index)") {{ area }}
        //- .slecter
        //-   .slecter__info
        //-     img.slecter__info__icon(src="../assets/images/theater.png")
        //-     span 影院 ：
        //-   .slecter__items
        //-     .slecter__items__item(v-for="(cinema, index) in cinemas", :class="index === cinemaSelect ? 'slecter__items__item--selected' : ''", @click="changeCinema(index)") {{ cinema.name }}
        .cinemas
          .cinema(v-for="(cinema, index) in cinemas")
            .cinema__info {{ cinema.name }}
            .cinema__op(@click="selectCinema(index)") 选座购票

    .seats(v-show="currentStep === 1")
      .back(@click="back")
        i.el-icon-arrow-left
        |  返回
      .confirm(@click="confirmSeats")
        |  确定
        i.el-icon-arrow-right
      .seat-tip
        .seat.seat-normal
        .seat-tip__text 可选座位
        .seat.seat--sale
        .seat-tip__text 已售座位
        .seat.seat--selected
        .seat-tip__text 已选座位
      .seat-container(v-loading="seatsLoading")
        .seat-row(v-for="(row, rowIndex) in seats")
          .seat(v-for="(seat, index) in row", :class="['seat', 'seat--sale', 'seat--selected'][seat]", @click="selectSeat(row, index, rowIndex)")
      img.seat-screen(src="../assets/images/screen.png")

    .order(v-show="currentStep === 2", v-loading="buying")
      .info
        .info__title 座位信息:
        .info__content
          .seat-item(v-for="seat in form.seats")
            .seat.seat--selected
            .seat-tip__text {{ seat.row }}行{{ seat.col }}列
      .info
        .info__title 影院信息:
        .info__content
          .info__content__text {{ form.cinema.name }}
      .info
        .info__title 时间信息:
        .info__content
          .info__content__text {{ form.time }}
      .info
        .info__title 金额信息:
        .info__content
          .info__content__text {{ form.money }}
      .order__op
        .order__op__item(@click="back") 返回
        .order__op__item(@click="comfirmOrder") 确认订单

    el-dialog(title="选择排场时间", v-model="timeSelectVisible", size="tiny")
      el-time-select(size="large", v-model="timeStamp", :picker-options="{ start: '08:30', step: '00:30', end: '22:30'}",placeholder="选择时间")
      span(slot="footer")
        el-button(@click="timeSelectVisible = false") 取 消
        el-button(type="primary", @click="selectTime") 确 定
</template>

<script>

import vue from 'vue'
import router from '@/router/index.js'
import { User, Movie, Cinema } from '@/models/index.js'

export default {
  name: 'hello',
  data () {
    return {
      timeSelectVisible: false,
      timeStamp: '',
      seatid: '',
      film: {},
      tabName: 'intro',
      seats: [],
      currentStep: 0,
      timeSelect: 0,
      times: ['今天', '明天', '后天'],
      areaSelect: 0,
      areas: ['番禺区', '白云区', '海珠区', '天河区', '荔湾区', '越秀区', '黄埔区', '花都区', '南沙区', '从化市', '增城市'],
      cinemaSelect: 0,
      cinemas: [],
      seatsLoading: false,
      buying: false,
      form: {
        cinema: '',
        time: '',
        seats: [],
        money: ''
      }
    }
  },
  created () {
    let id = this.$route.params.id
    Movie.fetchDtl(id).then(data => {
      this.film = data
    })
    this.changeArea(0)
  },
  methods: {
    changeTime (index) {
      this.timeSelect = index
    },
    changeArea (index) {
      this.areaSelect = index
      Cinema.fetchCinemaByArea(this.areas[index]).then(res => {
        this.cinemas = res
      })
    },
    changeCinema (index) {
      this.cinemaSelect = index
    },
    back () {
      this.currentStep = this.currentStep - 1
    },
    confirmSeats () {
      let seats = []
      for (let i = 0; i < this.seats.length; i++) {
        for (let j = 0; j < this.seats[i].length; j++) {
          if (this.seats[i][j] === 2) {
            seats.push({
              row: this.seats.length - i,
              col: j + 1
            })
          }
        }
      }
      if (seats.length === 0) {
        this.$alert('您尚未选择任何座位', '提示', {
          confirmButtonText: '确定'
        })
      } else {
        let seat = ''
        for (let i = 0; i < this.seats.length; i++) {
          seat += this.seats[i].join('').replace(/1/g, '0').replace(/2/g, '1')
        }
        User.lockSeat(this.seatid, { seat }).then(res => {
          if (res.stateCode === '200') {
            this.$message('锁定座位成功')
            this.form.seats = seats
            this.form.money = seats.length * 30 + '元'
            this.currentStep = this.currentStep + 1
          } else {
            throw new Error()
          }
        }).catch(() => {
          this.$message.error('锁定座位失败')
        })
      }
    },
    comfirmOrder () {
      let seat = ''
      for (let i = 0; i < this.seats.length; i++) {
        seat += this.seats[i].join('').replace(/1/g, '0')
      }
      this.buying = true
      User.buySeat(this.seatid, { seat }).then(res => {
        if (res.stateCode === '200') {
          this.$message('购买成功')
          router.push({ name: 'Home' })
        } else {
          throw new Error()
        }
        this.buying = false
      }).catch(() => {
        this.$message.error('购买失败')
        this.buying = false
      })
    },
    selectCinema (index) {
      this.form.cinema = this.cinemas[index]
      for (let i = 0; i < this.seats.length; i++) {
        for (let j = 0; j < this.seats[i].length; j++) {
          if (this.seats[i][j] === 2) {
            this.seats[i][j] = 0
          }
        }
      }
      this.timeSelectVisible = true
    },
    selectTime () {
      this.form.time = this.times[this.timeSelect] + this.timeStamp
      this.currentStep = 1
      this.timeSelectVisible = false

      let date = this.$moment().add(this.timeSelect, 'days').format('YYYYMMDD')
      let time = this.timeStamp
      this.seatsLoading = true
      Cinema.fetchSeat(this.form.cinema.id, this.$route.params.id, date, time).then(res => {
        let cinema = res[0]
        this.seatid = cinema.id
        let seats = cinema.seats + ''
        this.seats = []
        for (let row = 0; row < 8; row++) {
          this.seats.push([])
          for (let col = 0; col < 11; col++) {
            if (!seats[row * 11 + col] || seats[row * 11 + col] === '0') {
              this.seats[row].push(0)
            } else if (seats[row * 11 + col] === '1' || seats[row * 11 + col] === '2') {
              this.seats[row].push(1)
            }
          }
        }
        this.seatsLoading = false
      })
    },
    selectSeat (row, index, rowIndex) {
      if (row[index] === 0) {
        vue.set(row, index, 2)
      } else if (row[index] === 2) {
        vue.set(row, index, 0)
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .seats {
    min-height: 100px;
    margin-right: 500px;
    margin-left: 100px;
    margin-top: 100px;
    position: relative;
  }

  .booking__steps {
    position: relative;
    top: 50px;
    margin-right: 500px;
    margin-left: 100px;
  }

  .seat {
    background: url('../assets/images/normal.png') no-repeat;
    background-size: 26px 26px;
    height: 26px;
    width: 26px;
    display: inline-block;
    cursor: pointer;
  }

  .seat:not(.seat-normal):not(.seat--sale):not(.seat--selected):hover {
    background-image: url('../assets/images/hover.png');
  }

  .seat--sale {
    background-image: url('../assets/images/sale.png');
  }

  .seat--selected {
    background-image: url('../assets/images/selected.png');
  }

  .seat-tip__text {
    display: inline-block;
    line-height: 30px;
    vertical-align: top;
    padding-left: 8px;
    margin-right: 12px;
    font-size: 16px;
    font-weight: 500;
  }

  .seat-container {
    margin-top: 30px;
  }

  .seat-container .seat {
    margin: 0px 10px;
  }

  .seat-screen {
    width: 320px;
    margin-top: 40px;
    position: relative;
  }

  .booking-form {
    margin: 100px 500px 50px 100px;
  }

  .slecter {
    padding-top: 10px;
  }

  .slecter:first-child {
    padding-top: 0px;
  }

  .slecter__info {
    display: inline-block;
    float: left;
    width: 100px;
  }

  .slecter__info__icon {
    margin-right: 4px;
    height: 18px;
    width: 18px;
    vertical-align: top;
    margin-top: 2px;
  }

  .slecter__items {
    margin-left: 100px;
    overflow: auto;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
  }

  .slecter__items__item {
    display: inline-block;
    float: left;
    font-size: 14px;
    font-weight: 500;
    padding: 2px 8px;
    cursor: pointer;
  }

  .slecter__items__item--selected, .slecter__items__item:hover {
    background: #20a0ff;
    color: white;
  }

  .cinemas {
    margin-top: 20px;
  }

  .cinema {
    padding: 10px 0px;
    background: #55B7FF;
    color: #fff;
    margin-bottom: 2px;
    border-radius: 2px;
  }

  .cinema:hover {
    background: #55c3ff;
  }

  .cinema__info, .cinema__op {
    display: inline-block;
  }

  .cinema__info {
    margin-right: 100px;
    font-weight: 500;
  }

  .cinema__op {
    float: right;
    width: 100px;
    cursor: pointer;
  }

  .back, .confirm {
    text-align: left;
    color: #20a0ff;
    font-size: 16px;
    cursor: pointer;
    display: inline-block;
    position: absolute;
    font-weight: 500;
    top: 2px;
  }

  .back {
    margin-left: 65px;
    left: 0px;
  }

  .confirm {
    margin-right: 75px;
    right: 0px;
  }

  .order {
    position: relative;
    margin-top: 100px;
    margin-left: 100px;
    margin-right: 500px;
    border: 1px solid #d1dbe5;
    box-shadow: 0px 0px 4px #d1dbe5;
    padding: 20px 10px 10px 10px;
    border-radius: 4px;
  }

  .order__op {

  }

  .order__op__item {
    display: inline-block;
    width: 49%;
    font-weight: 700;
    padding: 8px 20px;
    box-sizing: border-box;
    cursor: pointer;
    margin: 0px 0.5%;
    border-radius: 2px;
    background: #20a0ff;
    color: #fff;
  }

  .info {
    overflow: auto;
    margin-bottom: 16px;
    line-height: 30px;
  }

  .info__title {
    width: 100px;
    display: inline-block;
    float: left;
    font-weight: bold;
  }

  .info__content {
    margin-left: 100px;
  }

  .info__content__text {
    font-weight: bold;
    text-align: left;
    margin-left: 10px;
  }

  .seat-item {
    display: inline-block;
    margin: 0px 10px;
    float: left;
  }

  .cinema-info {
    overflow: auto;
    text-align: left;
    font-weight: bold;
  }

  .film {
    float: right;
    margin-right: 140px;
    margin-top: 50px;
    margin-bottom: 50px;
    width: 230px;
    box-shadow: 0px 0px 6px #aaa;
    padding: 5px;
    padding-bottom: 20px;
  }

  .film__img-container {
    height: 320px;
    width: 230px;
    background: #fff;
  }

  .film__img-container__img {
    width: 100%;
    height: 100%;
  }

  .film__content {
    margin-top: 20px;
  }

  .film__content__title {
    font-weight: 700;
    font-size: 18px;
  }

  .film__content__subtitle {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 10px;
  }

  .film__content__info {
    font-size: 14px;
  }

</style>
