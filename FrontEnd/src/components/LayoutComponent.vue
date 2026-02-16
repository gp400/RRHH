src/layouts/Default.vue
<template>
  <v-app>

    <v-app-bar flat color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>Recursos Humanos</v-toolbar-title>
    </v-app-bar>

    <!-- Drawer -->
    <v-navigation-drawer
      v-model="drawer"
      app
      color="grey lighten-4"
    >
      <v-list nav>
        <v-list-item link v-for="drawerRoute in drawerRoutes" :key="drawerRoute.title" :to="drawerRoute.route">
          <div class="d-flex align-end">
            <v-list-item-icon>
              <v-icon size="18">{{ drawerRoute.icon }}</v-icon> 
            </v-list-item-icon>
            <v-list-item-title class="text-body-1 list-item-title">{{ drawerRoute.title }}</v-list-item-title>
          </div>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <div class="pa-3">
        <router-view />
      </div>
    </v-main>
  </v-app>
</template>

<style>
  .list-item-title {
    margin-bottom: 2.2px;
    margin-left: 5px
  }
</style>

<script setup lang="ts">
  import { ref } from 'vue'

  class DrawerRoutes {
    route: String;
    icon: String;
    title: String;
  }

  const drawer = ref(true);

  const drawerRoutes = ref<DrawerRoutes[]>([
    {
      route: '/competence',
      icon: 'mdi-head-snowflake-outline',
      title: 'Competencias'
    },
    {
      route: '/language',
      icon: 'mdi-translate-variant',
      title: 'Idiomas'
    },
    {
      route: '/training',
      icon: 'mdi-human-capacity-decrease',
      title: 'Capacitaciones'
    },
    {
      route: '/position',
      icon: 'mdi-account-tie',
      title: 'Puestos'
    },
    {
      route: '/department',
      icon: 'mdi-sitemap-outline',
      title: 'Departamentos'
    },
    {
      route: '/candidate',
      icon: 'mdi-account-search',
      title: 'Candidatos'
    },
    {
      route: '/employee',
      icon: 'mdi-badge-account',
      title: 'Empleados'
    },
  ])
</script>
