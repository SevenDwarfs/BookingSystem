<template lang="jade">
  .filter
    .results
      router-link.film(v-for="film in onsales", :to="{ name: 'FilmDetail', params: { id: film.id } }")
        img.film__img(:src="film.url")
        .film__info
          .film__info__name {{film.name}}
    .no(v-if="onsales.length === 0")
      h3 无相关电影
</template>

<script>

import { Movie } from '@/models/index.js'

export default {
  data () {
    return {
      onsales: []
    }
  },
  created () {
    Movie.search(this.$route.query.keyword).then(res => {
      this.onsales = res
      // if (res.id !== -1) this.onsales = [res]
      // else this.$message.error('不存在该电影')
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .filter {
    padding-top: 30px;
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

</style>
