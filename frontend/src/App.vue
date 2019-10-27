<template>
  <div id="app">
    <div class="bg"></div>

    

    <div class="content">
    <h1>Live Streaming with Logitech </h1>

    <h3>Switch Camera</h3>

    <div :class="{'onair': screen == '172.20.10.13', 'camera': true}" @click="changeScreen('172.20.10.13')">
      Camera 1 
      <!-- <small>(172.20.10.13)</small> -->
    </div>

    <div :class="{'onair': screen == '172.20.10.2', 'camera': true}" @click="changeScreen('172.20.10.2')">
      Camera 2
      <!-- <small>(172.20.10.13)</small> -->
    </div>

    {{screen}}

    </div>

  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'

import axios from 'axios'
axios.defaults.baseURL = 'http://172.20.10.7:5000'
// axios.defaults.headers.common['Content-Type'] = 'application/x-www-form-urlencoded'
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'

export default {
  name: 'app',
  data() {
    return {
      screen: '172.20.10.13',
    }
  },
  components: {
    // HelloWorld
  },
  methods: {
    changeScreen(value) {
      axios.post('/control', {
        'method': 'switch',
        'value': value
      }).then((data) => {
        this.screen = value
      }).catch((err) => {
        alert(err)
      })
    }
  }
}
</script>

<style>

body {
  margin: 0;
  padding: 0;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #fff;
  margin: 0;
  padding: 0;
  /* background: url('bg.png') center center; */
}

.bg {
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: 5;
  background-image: url('./assets/bg.png');
  background-position: 50%;
  background-repeat: no-repeat;
  background-size: cover;
}

.content {
    position: absolute;
    top: 50%;
    margin-top: -200px;
    text-align: center;
    z-index: 20;
    width: 100%;
}

.camera {
  display: block;
  width: 80%;
  margin: 20px auto;
  background: #fff;
  border: 1px solid #eee;
  color: #444;
  padding: 25px 0;
  border-radius: 10px;
  font-size: 30px;
  cursor: pointer;
}

.onair {
  background: #f56161;
  color: #fff;
}

</style>
