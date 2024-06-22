<template>
  <div>
    <h1 class="green">Participants</h1>
    <div class="participants">
        <span v-for="participant in participants" :key="participant.id" class="participant-card">
          <ParticipantContainer :participant="participant"/>
        </span>
    </div>
    <h1 class="green">Add a Participant</h1>
    <ParticipantForm/>


    <h1 class="green">Draws</h1>
    <button class="margin-bottom" type="submit" @click="drawGenerate">
      Create A New Draw!
    </button>
    <div v-for="draw in draws" :key="draw.id" class="draw-card">
      <p>Date: {{ new Date(draw.created_at) }}</p>
      <table>
        <tr>
          <th>Santa</th>
          <th>Santee</th>
        </tr>
        <tr v-for="pair in draw.pairs">
          <td>{{ participantGetById(pair.santa) }}</td>
          <td>{{ participantGetById(pair.santee) }}</td>
        </tr>
      </table>
    </div>

  </div>
</template>

<script>
import Multiselect from 'vue-multiselect';

import {
  participantsSet,
  drawsGet,
  drawCreate,
} from "@/services/home.js";
import ParticipantContainer from "@/components/ParticipantContainer.vue";
import {Participant} from "@/models/Participant.js";
import ParticipantForm from "@/components/ParticipantForm.vue";


export default {
  data() {
    return {
      draws: [],
      new_username: '',
      new_email: '',
      new_blacklisted: [],
      dataReady: false,
    };
  },
  computed: {
    participants() {
      return this.$store.state.participants
    }
  },
  components: {
    ParticipantContainer,
    ParticipantForm,
    Multiselect,
  },
  async beforeMount() {
    await this.participantsFetch().then(() => {
      // Fetch the Draws after the participants have been fetched
      this.drawsFetch();
    });
    // Set the dataReady flag to true to render the page
    this.dataReady = true;
  },
  methods: {
    async participantsFetch() {
      try {
        await participantsSet();
      } catch (error) {
        alert(JSON.stringify(error.response.data));
      }
    },
    participantGetById(id) {
      const p = this.participants.find(participant => participant.id === id);
      if (p) {
        return p.label;
      }
      return 'deleted';
    },
    drawsFetch() {
      drawsGet().then((response) => {
        this.draws = response;
      }).catch((error) => {
        alert(JSON.stringify(error.response.data))
      });
    },
    drawGenerate() {
      drawCreate().then((response) => {
        // Prepend the new draw to the list
        this.draws = [response].concat(this.draws);
      }).catch((error) => {
        alert(JSON.stringify(error.response.data))
      });
    },


  }
};
</script>

<style scoped>

.participants {
  width: fit-content;

}

.participant-card {
  display: inline-block;
  margin: 10px;
  white-space: nowrap;
}

.draw-card {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 8px;
}


</style>

