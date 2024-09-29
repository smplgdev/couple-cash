<template>
  <div>
      <p>{{platform}}</p>
      <AuthProvider :hex_hmac_signature="signature">
        <AppearanceProvider>
          <FormComponent />
        </AppearanceProvider>
      </AuthProvider>
  </div>
</template>

<script>
  import FormComponent from './components/FormComponent.vue';
  import { AppearanceProvider, AuthProvider } from '@erfanmola/televue';
  import '@erfanmola/televue/style.css';

  const webapp = window.Telegram.WebApp;

  export default {
    components: {
      AppearanceProvider,
      AuthProvider,
      FormComponent,
    },
    data() {
      return {
        signature: 'MY_SIGNATURE_HERE',
        platform: webapp.platform,
      };
    },
  };
</script>
