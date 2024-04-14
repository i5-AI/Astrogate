import preprocess from 'svelte-preprocess';
import adapter from '@sveltejs/adapter-static'; // or another appropriate adapter for your deployment

export default {
  kit: {
    adapter: adapter(),
  },
  preprocess: preprocess({
    postcss: true,
  }),
};
