<template lang="jade">
  .filter
    .selector-container
      .selector
        .selector__info 类型 :
        .selector__items
          .selector__item(v-for="(type, index) in types", :class="index === typeSelect ? 'selector__item--selected' : ''", @click="update('type', index)") {{ type }}
      //- .selector
      //-   .selector__info 区域 :
      //-   .selector__items
      //-     .selector__item(v-for="(area, index) in areas", :class="index === areaSelect ? 'selector__item--selected' : ''", @click="update('area', index)") {{ area }}
      .selector
        .selector__info 年代 :
        .selector__items
          .selector__item(v-for="(time, index) in times", :class="index === timeSelect ? 'selector__item--selected' : ''", @click="update('time', index)") {{ time }}
    .results(v-loading="loading")
      router-link.film(v-for="film in onsales", :to="{ name: 'FilmDetail', params: { id: film.id } }")
        img.film__img(:src="film.url")
        .film__info
          .film__info__name {{film.name}}
    .pages
      el-pagination(layout="prev, pager, next", :page-size="step", :total="total", @current-change="handleCurrentChange")
</template>

<script>

import { Movie } from '@/models/index.js'

export default {
  name: 'hello',
  data () {
    return {
      onsales: [],
      page: 0,
      step: 60,
      total: 0,
      loading: false,
      types: ['all', '爱情', '喜剧', '动画', '剧情', '恐怖', '惊悚', '科幻', '动作', '悬疑', '犯罪', '冒险', '战争', '奇幻', '运动', '家庭', '古装', '武侠', '西部', '历史', '传记', '情色', '歌舞', '黑色电影', '短片', '纪录片', '其他'],
      typeSelect: 0,
      areas: ['all', '大陆', '美国', '韩国', '日本', '中国香港', '中国台湾', '泰国', '印度', '法国', '英国', '俄罗斯', '意大利', '西班牙', '德国', '波兰', '澳大利亚', '伊朗', '其他'],
      areaSelect: 0,
      times: ['all', '2017', '2016', '2015', '2014', '2013', '2012', '2011'],
      timeSelect: 0
    }
  },
  created () {
    this.updateMovie()
  },
  methods: {
    update (_type, index) {
      this[_type + 'Select'] = index
      this.updateMovie()
    },
    updateMovie () {
      let type = this.types[this.typeSelect]
      let area = 'all'
      let time = this.times[this.timeSelect]
      this.loading = true
      Movie.queryMovie(type, area, time, this.page, this.step).then(res => {
        this.onsales = res
        this.loading = false
      }).catch(err => {
        this.loading = false
        this.$message.error(err.message)
      })
      Movie.countMovie(type, area, time).then(total => {
        this.total = total
      })
    },
    handleCurrentChange (current) {
      this.page = current - 1
      this.updateMovie()
      window.scroll(0, 0)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .filter {
    padding-top: 30px;
  }

  .selector-container {
    border: 1px solid #e5e5e5;
    margin: 30px 66px;
    padding: 20px;
  }

  .selector {
    overflow: auto;
    border-bottom: 1px solid #eee;
    padding-bottom: 20px;
    padding-top: 20px;
  }

  .selector:first-child {
    padding-top: 0px;
  }

  .selector:last-child {
    padding-bottom: 0px;
    border-bottom: none;
  }

  .selector__info {
    display: inline-block;
    float: left;
    width: 60px;
    text-align: left;
    font-size: 16px;
    color: gray;
    font-weight: 700;
    line-height: 30px;
  }

  .selector__items {
    margin-left: 60px;
    text-align: left;
  }

  .selector__item {
    display: inline-block;
    padding: 4px 12px;
    font-size: 14px;
    font-weight: 700;
    border-radius: 20px;
    cursor: pointer;
  }

  .selector__item:hover {
    color: #20a0ff;
  }

  .selector__item--selected, .selector__item--selected:hover {
    background: #20a0ff;
    color: #fff;
  }


  .results {
    padding: 10px;
    margin: 0px 46px;
    overflow: auto;
  }

  .film {
    display: inline-block;
    width: 160px;
    padding: 6px;
    border: 1px solid #e5e5e5;
    box-shadow: 0px 0px 4px #e5e5e5;
    background: #fff;
    margin: 10px;
    position: relative;
    text-decoration: none;
    color: #000;
  }

  .film__img {
    width: 100%;
    height: 220px;
    vertical-align: bottom;
    display: block;
  }

  .film__info {
    display: block;
    padding: 6px 0px;
  }

  .film__info__name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 16px;
    font-weight: 700;
  }

  .film:hover {
    background: #20a0ff;
    color: #fff;
    cursor: pointer;
    animation: inin 0.8s;
  }

  @keyframes inin {
    0% {
      top: 0px;
    }
    50% {
      top: 8px;
    }
    100% {
      top: 0px;
    }
  }

  .pages {
    margin-bottom: 40px;
    margin-top: 20px;
  }

</style>
