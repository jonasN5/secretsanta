<template>
  <form @submit.prevent="submit">
    <div class="mdl-card">
      <label class="input-label" for="username">Username: </label>
      <input class="margin-right" v-model="username" type="text"/>
      <label class="input-label" for="email">Email: </label>
      <input class="margin-right" v-model="email" type="email"/>
      <div>
        <label class="margin-bottom">Blacklist:</label>
        <multiselect v-model="blacklisted" :options="participants" :multiple="true"
                     :close-on-select="false"
                     :clear-on-select="false"
                     :selected="blacklisted"
                     :preserve-search="true" placeholder="Select participants" label="email" track-by="id">
          <template #selection="{ values, search, isOpen }">
            <span class="multiselect__single"
                  v-if="values.length"
                  v-show="!isOpen">{{ values.length }} participant(s) blacklisted</span>
          </template>
        </multiselect>
      </div>
      <div class="margin-top margin-bottom">
        <button type="submit" @click="participantAdd" v-if="!participantExisting">
          Add
        </button>
        <button class="margin-right" type="submit" @click="participantUpdate" v-if="participantExisting">
          Update
        </button>
        <button @click="cancelEdit" v-if="participantExisting">
          Cancel
        </button>
      </div>
    </div>


  </form>
</template>

<script>
import {Participant} from "@/models/Participant.js";
import {participantCreate, participantUpdate} from "@/services/home.js";
import IconTrash from "@/assets/icons/IconTrash.vue";
import IconEdit from "@/assets/icons/IconEdit.vue";
import Multiselect from "vue-multiselect";


export default {
  props: {
    participantExisting: Participant,
  },
  data() {
    return {
      username: this.participantExisting?.username ?? '',
      email: this.participantExisting?.email ?? '',
      blacklisted: this.participantExisting?.blacklisted ?? [],
    };
  },
  computed: {
    participants() {
      if (this.participantExisting) {
        // Prevent the participant from blacklisting themselves
        return this.$store.state.participants.filter(participant => participant.id !== this.participantExisting.id);
      }
      return this.$store.state.participants
    }
  },
  components: {
    Multiselect,
    IconEdit,
    IconTrash,
  },
  methods: {
    participantAdd() {
      participantCreate(this.username, this.email, this.blacklisted).then((response) => {
        this.participantFormClear();
      }).catch((error) => {
        alert(JSON.stringify(error.response.data))
      });
    },
    participantFormClear() {
      this.username = '';
      this.email = '';
      this.blacklisted = [];
    },
    participantUpdate() {
      this.participantExisting.username = this.username;
      this.participantExisting.email = this.email;
      this.participantExisting.blacklisted = this.blacklisted;
      participantUpdate(this.participantExisting).then((response) => {
        this.cancelEdit();
      }).catch((error) => {
        alert(JSON.stringify(error.response.data))
      });
    },
    cancelEdit() {
      this.$emit('edit-finished');
    },
  }
}
</script>


<style src="../../node_modules/vue-multiselect/dist/vue-multiselect.css"></style>

<style>
.multiselect {
  max-width: 800px;
}
</style>