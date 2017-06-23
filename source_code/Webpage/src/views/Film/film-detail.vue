<template lang="jade">
  .film
    .film__header
      .film__header__img-container
        img.film__header__img-container__img(:src="film.url")
      .film__header__content
        .film__header__content__title {{ film.chineseName }}
        .film__header__content__subtitle {{ film.englishName }}
        .film__header__content__info {{ film.type }}
        .film__header__content__info {{ film.length }}
        .film__header__content__info {{ film.releaseDate }} {{ film.showPlace }}
        .film__header__content__rating 评分: {{ film.rating }}
        router-link.film__header__content__operation(:to="{ name: 'Booking', params: { id: film.id } }") 立刻购票

    el-tabs.film__body(v-model="tabName")
      el-tab-pane(label="介绍", name="intro")
        .film__body__title 剧情简介
        .film__body__content {{ film.introduction }}
      el-tab-pane(label="演职人员", name="people")
        .film__body__title 导演
        .film__body__content
          .film-man(v-for="item in film.directors")
            img.film-man__avatar(:src="item.url")
            .film-man__name {{ item.name }}
        .film__body__title 演员
        .film__body__content
          .film-man(v-for="item in film.actors")
            img.film-man__avatar(:src="item.url")
            .film-man__name {{ item.name }}
      el-tab-pane(label="图集", name="pic")
        img.film-img(v-for="pic in film.pictures", :src="pic.url")

</template>

<script>

import { Movie } from '@/models/index.js'

export default {
  name: 'hello',
  data () {
    return {
      film: {},
      tabName: 'intro'
    }
  },
  created () {
    let id = this.$route.params.id
    Movie.fetchDtl(id).then(data => {
      this.film = data
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .film__header {
    background: #392f59 url(https://ms0.meituan.net/mywww/banner_bg.f7fd103e3b8c16b6f449cce43fc57f45.png) no-repeat 50%;
    position: relative;
    height: 376px;
  }

  .film__header__img-container {
    height: 320px;
    width: 230px;
    padding: 5px;
    background: #fff;
    box-shadow: 0px 0px 4px gray;
    position: absolute;
    left: 100px;
    bottom: -20px;
  }

  .film__header__img-container__img {
    width: 100%;
    height: 100%;
  }

  .film__header__content {
    position: absolute;
    left: 400px;
    top: 70px;
    color: #fff;
    text-align: left;
  }

  .film__header__content__title {
    margin-top: 0;
    font-size: 26px;
    line-height: 32px;
    font-weight: 700;
  }

  .film__header__content__subtitle {
    font-size: 18px;
    line-height: 1.3;
    margin-bottom: 14px;
    font-weight: 700;
  }

  .film__header__content__info {
    font-size: 16px;
    line-height: 22px;
  }

  .film__header__content__rating {
    position: relative;
    color: #ffb400;
    font-weight: bold;
    font-size: 22px;
    font-style: italic;
    margin-top: 20px;
    margin-bottom: 30px;
  }

  .film__header__content__operation {
    width: 250px;
    height: 40px;
    font-size: 16px;
    line-height: 40px;
    text-align: center;
    border-radius: 2px;
    background: #20a0ff;
    cursor: pointer;
    font-weight: 500;
    display: block;
    text-decoration: none;
    color: #fff;
  }

  .film__body {
    margin-top: 60px;
    padding: 0px 10px 0px 100px;
  }

  .film__body__title {
    border-left: 6px solid #20a0ff;
    text-align: left;
    padding-left: 6px;
    font-size: 20px;
    font-weight: 700;
    margin: 20px 0px;
  }

  .film__body__content {
    font-size: 14px;
    margin-bottom: 40px;
    text-align: left;
    margin-right: 40px;
  }

  .film-man {
    width: 150px;
    padding: 4px;
    border-radius: 4px;
    display: inline-block;
    margin-right: 40px;
  }

  .film-man__avatar {
    width: 100%;
    border-radius: 2px;
  }

  .film-man__name, .film-man__role {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    text-align: center;
  }

  .film-man__name {
    max-width: 100%;
    font-size: 16px;
    font-weight: 500;
    margin-bottom: 4px;
  }

  .film-man__role {
    font-size: 12px;
  }

  .film-img {
    width: 126px;
    height: 126px;
    display: inline-block;
    float: left;
    margin: 10px 20px 10px 0px;
  }

</style>
