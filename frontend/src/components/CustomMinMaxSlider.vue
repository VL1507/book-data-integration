<script setup>
import { computed, ref, watchEffect } from 'vue'

// define component props for the slider component
const { min, max, step, minValue, maxValue } = defineProps({
  min: {
    type: Number,
    default: 0,
  },
  max: {
    type: Number,
    default: 100,
  },
  step: {
    type: Number,
    default: 1,
  },
  minValue: {
    type: Number,
    default: 50,
  },
  maxValue: {
    type: Number,
    default: 80,
  },
})

// define emits for the slider component
const emit = defineEmits(['update:minValue', 'update:maxValue'])

// define refs for the slider element and the slider values
const slider = ref(null)
const sliderMinValue = ref(minValue)
const sliderMaxValue = ref(maxValue)

// function to get the percentage of a value between the min and max values
const getPercent = (value, min, max) => {
  return ((value - min) / (max - min)) * 100
}

// function to get the difference between the min and max values
const sliderDifference = computed(() => {
  return Math.abs(sliderMaxValue.value - sliderMinValue.value)
})

// function to set the css variables for width, left, and right
const setCSSProps = (width, left, right) => {
  slider.value.style.setProperty('--width', `${width}%`)
  slider.value.style.setProperty('--progressLeft', `${left}%`)
  slider.value.style.setProperty('--progressRight', `${right}%`)
}

// watchEffect to emit the updated values, and update the css variables
// when the slider values change
watchEffect(() => {
  if (slider.value) {
    // emit slidet values when updated
    emit('update:minValue', sliderMinValue.value)
    emit('update:maxValue', sliderMaxValue.value)

    // calculate values in percentages
    const differencePercent = getPercent(sliderDifference.value, min, max)
    const leftPercent = getPercent(sliderMinValue.value, min, max)
    const rightPercent = 100 - getPercent(sliderMaxValue.value, min, max)

    // set the CSS variables
    setCSSProps(differencePercent, leftPercent, rightPercent)
  }
})
</script>
<template>
  <div ref="slider" class="custom-slider minmax">
    <input
      type="range"
      name="min"
      id="min"
      :min="min"
      :max="max"
      :value="minValue"
      :step="step"
      @input="({ target }) => (sliderMinValue = parseFloat(target.value))"
    />
    <input
      type="range"
      name="max"
      id="max"
      :min="min"
      :max="max"
      :value="maxValue"
      :step="step"
      @input="({ target }) => (sliderMaxValue = parseFloat(target.value))"
    />
  </div>
  <div class="minmax-inputs">
    <input type="number" :step="step" v-model="sliderMinValue" />
    <input type="number" :step="step" v-model="sliderMaxValue" />
  </div>
</template>

<style scoped>
.custom-slider {
  --trackHeight: 0.5rem;
  --thumbRadius: 1rem;
}

/* СЛАЙДЕР */
.custom-slider input[type="range"] {
  position: relative;
  appearance: none;
  /* pointer-events: none; */
  border-radius: 999px;
  z-index: 0;
}

/* ЗАМЕНА ПОЛОСЫ НА ЯРКИЙ ЗЕЛЕНЫЙ ЦВЕТ */
.custom-slider input[type="range"]::before {
  content: "";
  position: absolute;
  width: var(--ProgressPercent, 100%);
  height: 100%;
  background: #00865a;
  z-index: -3;
  pointer-events: none;
  border-radius: 999px;
}

/* `::-webkit-slider-runnable-track` targets the track (background) of a range slider in chrome and safari browsers. */
.custom-slider input[type="range"]::-webkit-slider-runnable-track {
  appearance: none;
  background: #005a3c;
  height: var(--trackHeight);
  border-radius: 999px;
}

/* `::-moz-range-track` targets the track (background) of a range slider in Mozilla Firefox. */
.custom-slider input[type="range"]::-moz-range-track {
  appearance: none;
  background: #005a3c;
  height: var(--trackHeight);
  border-radius: 999px;
}


/* РУЧКа */
.custom-slider input[type="range"]::-webkit-slider-thumb {
  position: relative;
  /* top: 50%;
  transform: translate(0, -50%);
  */
  width: var(--thumbRadius);
  height: var(--thumbRadius);
  margin-top: calc((var(--trackHeight) - var(--thumbRadius)) / 2);
  background: #00bd7e;
  border-radius: 999px;
  pointer-events: all;
  appearance: none;
  z-index: 10;
}


/* МОДИФИКАЦИЯ ПРЕДЫДУЩЕГО В ДВА СЛАЙДЕРА С ДВУМЯ РУЧКАМИ */
.custom-slider.minmax input[type="range"] {
  position: absolute;
  pointer-events: none;
  width: 14%;
}
.custom-slider.minmax input[type="range"]::-webkit-slider-runnable-track {
  background: none;
}

.custom-slider.minmax::before {
  left: var(--progressLeft);
  right: var(--progressRight);
  width: unset;
}

.custom-slider.minmax input[type="range"]::before {
  display: none;
}

.minmax-inputs {
  display: flex;
  justify-content: space-between;
}

.minmax-inputs input {
  width: 50px;
}
</style>