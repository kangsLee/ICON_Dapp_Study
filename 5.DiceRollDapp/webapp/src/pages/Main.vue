<template>
  <App>
    <div class="contents">
      <div class="dice-container">
        <div class="dice">
          <div class="side front">
            <div v-show="dice == 0">
              <div class="dot center"></div>
            </div>
            <div v-show="dice == 1">
              <div class="dot dtop dleft"></div>
              <div class="dot dbottom dright"></div>
            </div>
            <div v-show="dice == 2">
              <div class="dot dtop dleft"></div>
              <div class="dot center"></div>
              <div class="dot dbottom dright"></div>
            </div>
            <div v-show="dice == 3">
              <div class="dot dtop dleft"></div>
              <div class="dot dtop dright"></div>
              <div class="dot dbottom dleft"></div>
              <div class="dot dbottom dright"></div>
            </div>
            <div v-show="dice == 4">
              <div class="dot center"></div>
              <div class="dot dtop dleft"></div>
              <div class="dot dtop dright"></div>
              <div class="dot dbottom dleft"></div>
              <div class="dot dbottom dright"></div>
            </div>
            <div v-show="dice == 5">
              <div class="dot dtop dleft"></div>
              <div class="dot dtop dright"></div>
              <div class="dot dbottom dleft"></div>
              <div class="dot dbottom dright"></div>
              <div class="dot center dleft"></div>
              <div class="dot center dright"></div>
            </div>
          </div>
          <div class="side front inner"></div>
          <div class="side top">
            <div class="dot dtop dleft"></div>
            <div class="dot dbottom dright"></div>
          </div>
          <div class="side top inner"></div>
          <div class="side right">
            <div class="dot dtop dleft"></div>
            <div class="dot center"></div>
            <div class="dot dbottom dright"></div>
          </div>
          <div class="side right inner"></div>
          <div class="side left">
            <div class="dot dtop dleft"></div>
            <div class="dot dtop dright"></div>
            <div class="dot dbottom dleft"></div>
            <div class="dot dbottom dright"></div>
          </div>
          <div class="side left inner"></div>
          <div class="side bottom">
            <div class="dot center"></div>
            <div class="dot dtop dleft"></div>
            <div class="dot dtop dright"></div>
            <div class="dot dbottom dleft"></div>
            <div class="dot dbottom dright"></div>
          </div>
          <div class="side bottom inner"></div>
          <div class="side back">
            <div class="dot dtop dleft"></div>
            <div class="dot dtop dright"></div>
            <div class="dot dbottom dleft"></div>
            <div class="dot dbottom dright"></div>
            <div class="dot center dleft"></div>
            <div class="dot center dright"></div>
          </div>
          <div class="side back inner"></div>
          <div class="side cover x"></div>
          <div class="side cover y"></div>
          <div class="side cover z"></div>
        </div>
      </div>
      <button class="ui button primary" @click="roll">굴리기</button>
    </div>
  </App>
</template>

<script>
import App from "../layouts/App";
import IconService from "icon-sdk-js";

const httpProvider = new IconService.HttpProvider(
  "https://bicon.net.solidwallet.io/api/v3"
);
const iconService = new IconService(httpProvider);
export default {
  name: "home",
  data() {
    return {
      dice: 0
    };
  },
  components: {
    App
  },
  methods: {
    executeCallMethod() {
      const call = new IconService.IconBuilder.CallBuilder()
        .to("cx201353b6481da331c10a87067418a2270f873176")
        .method("diceRoll")
        .params({ name: Math.random().toString() })
        .build();
      return iconService.call(call).execute();
    },
    roll() {
      const rollAudio = new Audio("/static/sounds/roll.mp3");
      rollAudio.play();
      $(".dice").addClass("rolling");
      this.executeCallMethod().then(number => {
        this.dice = number;
      });
      setTimeout(() => {
        $(".dice").removeClass("rolling");
      }, 800);
    }
  }
};
</script>

<style lang="scss" scoped>
.contents {
  margin: 0 auto;
  max-width: 710px;
  button {
    display: block;
    margin: 0 auto;
  }
  .dice-container {
    margin-top: 100px;
    height: 300px;
  }
  .dice {
    margin: 0 auto;
    width: 200px;
    height: 200px;
    display: block;
    -webkit-transform-style: preserve-3d;
    transform-style: preserve-3d;
    &.rolling {
      -webkit-animation: spin 2s linear infinite;
      animation: spin 2s linear infinite;
    }

    .inner {
      background: #e0e0e0;
      box-shadow: none;
    }

    .dot {
      position: absolute;
      width: 46px;
      height: 46px;
      border-radius: 23px;
      background: #444;
      box-shadow: inset 5px 0 10px #000;

      &.center {
        margin: 77px 0 0 77px;
      }
      &.dtop {
        margin-top: 20px;
      }
      &.dleft {
        margin-left: 134px;
      }
      &.dright {
        margin-left: 20px;
      }
      &.dbottom {
        margin-top: 134px;
      }
      &.center.dleft {
        margin: 77px 0 0 20px;
      }
      &.center.dright {
        margin: 77px 0 0 134px;
      }
    }

    .front {
      -webkit-transform: translateZ(100px);
      transform: translateZ(100px);

      &.inner {
        -webkit-transform: translateZ(98px);
        transform: translateZ(98px);
      }
    }
    .top {
      -webkit-transform: rotateX(90deg) translateZ(100px);
      transform: rotateX(90deg) translateZ(100px);
      &.inner {
        -webkit-transform: rotateX(90deg) translateZ(98px);
        transform: rotateX(90deg) translateZ(98px);
      }
    }
    .left {
      -webkit-transform: rotateY(-90deg) translateZ(100px);
      transform: rotateY(-90deg) translateZ(100px);
      &.inner {
        -webkit-transform: rotateY(-90deg) translateZ(98px);
        transform: rotateY(-90deg) translateZ(98px);
      }
    }
    .right {
      -webkit-transform: rotateY(90deg) translateZ(100px);
      transform: rotateY(90deg) translateZ(100px);
      &.inner {
        -webkit-transform: rotateY(90deg) translateZ(98px);
        transform: rotateY(90deg) translateZ(98px);
      }
    }
    .back {
      -webkit-transform: rotateX(-180deg) translateZ(100px);
      transform: rotateX(-180deg) translateZ(100px);
      &.inner {
        -webkit-transform: rotateX(-180deg) translateZ(98px);
        transform: rotateX(-180deg) translateZ(98px);
      }
    }
    .bottom {
      -webkit-transform: rotateX(-90deg) translateZ(100px);
      transform: rotateX(-90deg) translateZ(100px);
      &.inner {
        -webkit-transform: rotateX(-90deg) translateZ(98px);
        transform: rotateX(-90deg) translateZ(98px);
      }
    }

    .cover {
      border-radius: 0;
      -webkit-transform: translateZ(0);
      transform: translateZ(0);
      background: #e0e0e0;
      box-shadow: none;
      &.x {
        transform: rotateY(90deg);
      }
      &.z {
        transform: rotateX(90deg);
      }
    }
    .side {
      position: absolute;
      width: 200px;
      height: 200px;

      background: #fff;
      box-shadow: inset 0 0 40px #ccc;
    }
  }
}

@keyframes spin {
  0% {
    -webkit-transform: translateZ(-100px) rotateX(0deg) rotateY(0deg)
      rotate(0deg);
    transform: translateZ(-100px) rotateX(0deg) rotateY(0deg) rotate(0deg);
  }

  16% {
    -webkit-transform: translateZ(-100px) rotateX(180deg) rotateY(180deg)
      rotate(0deg);
    transform: translateZ(-100px) rotateX(180deg) rotateY(180deg) rotate(0deg);
  }

  33% {
    -webkit-transform: translateZ(-100px) rotateX(1turn) rotateY(90deg)
      rotate(180deg);
    transform: translateZ(-100px) rotateX(1turn) rotateY(90deg) rotate(180deg);
  }

  50% {
    -webkit-transform: translateZ(-100px) rotateX(1turn) rotateY(1turn)
      rotate(1turn);
    transform: translateZ(-100px) rotateX(1turn) rotateY(1turn) rotate(1turn);
  }

  66% {
    -webkit-transform: translateZ(-100px) rotateX(180deg) rotateY(1turn)
      rotate(270deg);
    transform: translateZ(-100px) rotateX(180deg) rotateY(1turn) rotate(270deg);
  }

  83% {
    -webkit-transform: translateZ(-100px) rotateX(270deg) rotateY(180deg)
      rotate(180deg);
    transform: translateZ(-100px) rotateX(270deg) rotateY(180deg) rotate(180deg);
  }

  to {
    -webkit-transform: translateZ(-100px) rotateX(1turn) rotateY(1turn)
      rotate(1turn);
    transform: translateZ(-100px) rotateX(1turn) rotateY(1turn) rotate(1turn);
  }
}
</style>