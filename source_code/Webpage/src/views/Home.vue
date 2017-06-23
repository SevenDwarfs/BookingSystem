<template lang="jade">
.home
  el-carousel.slide(:interval="5000", arrow="always", height="440px")
    el-carousel-item(v-for="img in imgs")
      img.slide__img(:src="img.src")
  .main
    .movie-grid(v-loading="newsLoading")
      .movie-grid__header
        .movie-grid__header__title 最新上映（{{newFilms.length}}部）
      .movie-grid__content
        .movie-item(v-for="film in newFilms")
          img.movie-item__img(:src="film.url")
          .movie-item__bg
          .movie-item__info
            .movie-item__info__name {{film.name}}
            span.movie-item__info__point {{film.rating}}
          router-link.movie-item__operation(:to="{ name: 'FilmDetail', params: { id: film.id } }") 购票
    .movie-grid(v-loading="monthLoading")
      .movie-grid__header
        .movie-grid__header__title 本月上映（{{monthFilms.length}}部）
      .movie-grid__content
        .movie-item(v-for="film in monthFilms")
          img.movie-item__img(:src="film.url")
          .movie-item__bg
          .movie-item__info
            .movie-item__info__name {{film.name}}
            span.movie-item__info__point {{film.rating}}
          router-link.movie-item__operation(:to="{ name: 'FilmDetail', params: { id: film.id } }") 购票


</template>

<script>

import { Movie } from '@/models/index.js'

export default {
  name: 'hello',
  data () {
    return {
      imgs: [{
        src: 'http://p1.meituan.net/mmc/3c4f6e4b48387aa4a49f255ba447fe61144777.jpg'
      }, {
        src: 'http://p1.meituan.net/mmc/64fad7974cfd6c2136a31fa2bd8b4682129029.jpg'
      }, {
        src: 'http://p0.meituan.net/mmc/81fc61644a836fdd828aef5eda93a6e6116066.jpg'
      }],
      newsLoading: true,
      newFilms: [],
      monthLoading: true,
      monthFilms: []
    }
  },
  created () {
    Movie.fetchNews(18).then(data => {
      this.newFilms = data
      this.newsLoading = false
    })
    Movie.fetchMonth().then(data => {
      this.monthFilms = data
      this.monthLoading = false
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .slide {
    overflow: hidden;
  }

  .slide .slide__img {
    color: #475669;
    opacity: 0.75;
    margin: 0;
  }

  .main {
    width: 100%;
  }

  .movie-grid {
    position: relative;
    margin: 60px 100px;
    overflow: auto;
  }

  .movie-grid .movie-grid__header {
    width: 100%;
    height: 40px;
    line-height: 40px;
    color: #20a0ff;
  }

  .movie-grid__header .movie-grid__header__title {
    font-size: 24px;
    position: absolute;
    left: 0px;
    font-weight: bold;
    padding-left: 8px;
  }

  .movie-item {
    display: inline-block;
    border: 1px solid #efefef;
    margin: 8px;
    position: relative;
    float: left;
  }

  .movie-item:hover {
    box-shadow: 0 0 8px #fff, 0 5px 13px rgba(0,0,0,.07);
  }

  .movie-item .movie-item__img {
    width: 160px;
    height: 220px;
    font-size: 0px;
    vertical-align: bottom;
    box-shadow: 0 0px 20px #000 inset;
  }

  .movie-item .movie-item__bg {
    position: absolute;
    top: 0px;
    left: 0px;
    width: 160px;
    height: 220px;
    background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAABQCAMAAACpg44GAAAAbFBMVEUiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiIiK2HsfSAAAAJHRSTlPMxr63q6OahzclHRULBgHCsZOOf3p1cGtmYVxXUk1IQz4wLBAszz8hAAAAhklEQVRo3u3OxY0DAAADsBxDmZn337FTVPIjnsAZ4/zgCOcHhzg/+MBlgPOD/zg/+Ifzg3dcbrj84vzgFZcLLmdcTrgccTngssdlh8sWlw0ua1xWuCxxWeDyg/ODc1xmuHzj/OAXzg9+4vzgFJcPnB98x/nBCS5vOD9YVVVVVVVVVVVVr/IEUdzLcLhtP2AAAAAASUVORK5CYII=) repeat-x bottom;
  }

  .movie-item .movie-item__operation {
    width: 100%;
    height: 40px;
    line-height: 40px;
    color: #20a0ff;
    cursor: pointer;
    display: block;
    text-decoration: none;
  }

  .movie-item .movie-item__info {
    position: absolute;
    bottom: 50px;
    width: 100%;
  }

  .movie-item__info .movie-item__info__name {
    font-weight: bold;
    color: white;
    font-size: 16px;
    display: inline-block;
    float: left;
    padding-left: 8px;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    max-width: 60px;
  }

  .movie-item__info .movie-item__info__point {
    position: absolute;
    right: 8px;
    color: #ffb400;
    font-weight: bold;
    font-size: 1.2em;
    top: 0px;
    font-style: italic;
  }

  .movie-item .movie-item__operation:hover {
    color: white;
    background-color: #20a0ff;
  }

</style>
