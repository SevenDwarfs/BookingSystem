<template lang="jade">
  #app
    #nav
      #nav__logo
        router-link(:to="{ name: 'Home' }")
          img.nav__logo__icon(src="./assets/logo.png")
      #nav__login
        img(src="http://p0.meituan.net/movie/7dd82a16316ab32c8359debdb04396ef2897.png")
        el-dropdown.nav__login__dropdown(@command="handleUserCommand")
          i.el-icon-arrow-down
          el-dropdown-menu(slot="dropdown")
            el-dropdown-item(command="login", v-if="!hasLogin") 登录
            el-dropdown-item(command="register", v-if="!hasLogin") 注册
            el-dropdown-item(command="userorders", v-if="hasLogin") 查询订单
            el-dropdown-item(command="userinfo", v-if="hasLogin") 个人信息
            el-dropdown-item(command="logout", v-if="hasLogin") 退出
      el-input#nav__search(placeholder="找影视剧、影人、影院", v-model="searchText", icon="search", size="large", :on-icon-click="search")
      el-menu#nav__menu(:default-active="active", class="el-menu-demo", mode="horizontal")
        router-link(:to="{ name: 'Home' }")
          el-menu-item(index="0") 首页
        router-link(:to="{ name: 'FilmFilter' }")
          el-menu-item(index="1") 电影
        //- router-link(:to="{ name: 'FilmFilter' }")
        //-   el-menu-item(index="2") 榜单
        //- router-link(:to="{ name: 'Home' }")
        //-   el-menu-item(index="3") 热点
    #view
      router-view
    el-dialog(title="用户登录", v-model="loginDialogVisible")
      el-form(:model="loginForm", :rules="loginRules", ref="loginForm", label-width="72px", label-position="left")
        el-form-item(label="用户名", prop="username")
          el-input(v-model="loginForm.username")
        el-form-item(label="密码", prop="password")
          el-input(type="password", v-model="loginForm.password")
      span(slot="footer")
        el-button(@click="loginDialogVisible = false") 取 消
        el-button(type="primary", @click="login") 确 定
</template>

<script>

import router from '@/router/index.js'
import { User } from '@/models/index.js'

export default {
  name: 'app',
  data () {
    return {
      active: '0',
      searchText: '',
      loginDialogVisible: false,
      hasLogin: false,
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 6, max: 100, message: '用户名长度最低为6位', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 100, message: '密码长度最低为6位', trigger: 'blur' }
        ]
      }
    }
  },
  created () {
    let routes = router.options.routes
    for (let i = 0; i < routes.length; i++) {
      if (routes[i].name === this.$route.name) this.active = routes[i].active + ''
    }
    User.fetchInfo().then(res => {
      if (res.userName) this.hasLogin = true
    }).catch(() => {
      if (this.$route.name === 'Booking') this.navHome()
    })
  },
  methods: {
    search () {
      router.push({ name: 'FilmSearch', query: { keyword: this.searchText } })
    },
    navHome () {
      router.push({ name: 'Home' })
      this.loginDialogVisible = true
    },
    handleUserCommand (command) {
      if (command === 'login') {
        this.loginDialogVisible = true
      } else if (command === 'register') {
        router.push({ name: 'Register' })
      } else if (command === 'logout') {
        this.logout()
      } else if (command === 'userinfo') {
        router.push({ name: 'Profile' })
      } else if (command === 'userorders') {
        router.push({ name: 'Order' })
      }
    },
    login () {
      this.$refs['loginForm'].validate((valid) => {
        if (valid) {
          User.login(this.loginForm).then(res => {
            if (res.stateCode !== '200') {
              this.$message({
                message: res.info,
                type: 'error'
              })
            } else {
              this.$message({
                message: '登陆成功',
                type: 'success'
              })
              this.hasLogin = true
              this.loginDialogVisible = false
            }
          })
        } else {
          this.$message.error('表单错误')
        }
      })
    },
    logout () {
      User.logout().then(res => {
        if (res.stateCode === '200') {
          this.$message({
            message: '退出成功',
            type: 'success'
          })
          this.hasLogin = false
        } else {
          this.$message.error('登出失败, ' + res.info)
        }
      })
    }
  },
  watch: {
    '$route' (to, from) {
      let routes = router.options.routes
      for (let i = 0; i < routes.length; i++) {
        if (routes[i].name === to.name) this.active = routes[i].active + ''
      }
      if (to.name === 'Booking' && !this.hasLogin) {
        router.push({ name: from.name })
        this.loginDialogVisible = true
      }
    }
  }
}
</script>

<style>

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  min-width: 1240px;
}

#nav {
  height: 80px;
  background-color: #eef1f6;
  box-shadow: 0px 0px 8px rgba(0, 0, 0, .5);
  position: fixed;
  top: 0px;
  width: 100%;
  z-index: 100;
  min-width: 1240px;
}

#nav__menu {
  margin-left: 300px;
  height: 100%;
  margin-right: 360px;
}

#nav__menu .el-menu-item {
  height: 100%;
  line-height: 80px;
  width: 100px;
}

#nav__menu .is-active {
  border-bottom: 5px solid #20a0ff;
}

#nav__logo {
  height: 100%;
  width: 300px;
  float: left;
}

#nav__logo a {
  font-size: 40px;
  line-height: 80px;
  color: #20a0ff;
}

#nav__logo .nav__logo__icon {
  width: 60px;
  height: 60px;
  vertical-align: middle;
}

#nav__search {
  float: right;
  display: block;
  width: 220px;
  margin-top: 20px;
  margin-right: 20px;
  border-radius: 20px;
}

#nav__login {
  float: right;
  margin: 20px 40px 0px 40px;
  padding: 0px;
  position: relative;
  cursor: pointer;
}

#nav__login img {
  width: 40px;
  height: 40px;
  box-sizing: border-box;
  border-radius: 50%;
}

#nav__login .nav__login__dropdown {
  position: absolute;
  top: 15px;
  right: -28px;
  font-size: 16px;
}

#view {
  clear: both;
  margin-top: 80px;
}

/* 初始化样式 */
body, h1, h2, h3, h4, h5, h6, hr, p, blockquote, dl, dt, dd, ul, ol, li, pre, form, fieldset, legend, button, input, textarea, th, td { margin:0; padding:0; } body, button, input, select, textarea { font:12px/1.5tahoma, arial, \5b8b\4f53; } h1, h2, h3, h4, h5, h6{ font-size:100%; } address, cite, dfn, em, var { font-style:normal; } code, kbd, pre, samp { font-family:couriernew, courier, monospace; } small{ font-size:12px; } ul, ol { list-style:none; } a { text-decoration:none; } a:hover { text-decoration:underline; } sup { vertical-align:text-top; } sub{ vertical-align:text-bottom; } legend { color:#000; } fieldset, img { border:0; } button, input, select, textarea { font-size:100%; } table { border-collapse:collapse; border-spacing:0; }
a:link, a:active, a:hover, a:visited {
  text-decoration: none;
}

</style>
