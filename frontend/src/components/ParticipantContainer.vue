<template>
  <div class="container-participant" v-if="!isEditing">
    <div class="details">
      <p>{{ participant.label }}</p>
      <p>Blacklist: {{ participant.blacklisted.map(p => p.label).join(', ') }}</p>
    </div>
    <IconEdit class="icon" @click="onEditClicked"></IconEdit>
    <IconTrash class="icon" @click="onDeleteClicked"></IconTrash>
  </div>
  <ParticipantForm :participantExisting="participant" v-if="isEditing" @edit-finished="onEditFinished"/>
</template>

<script>
import IconTrash from "@/assets/icons/IconTrash.vue";
import IconEdit from "@/assets/icons/IconEdit.vue";
import {Participant} from "@/models/Participant.js";
import ParticipantForm from "@/components/ParticipantForm.vue";
import {participantDelete} from "@/services/home.js";

export default {
  props: {
    participant: Participant,
  },
  data() {
    return {
      isEditing: false,
    };
  },
  components: {
    ParticipantForm,
    IconEdit,
    IconTrash,
  },
  methods: {
    onEditClicked() {
      // Show the form and hide the details
      this.isEditing = true;
    },
    onEditFinished() {
      // Hide the form and show the details
      this.isEditing = false;
    },
    onDeleteClicked() {
      participantDelete(this.participant.id).then((response) => {
      }).catch((error) => {
        alert(JSON.stringify(error.response.data))
      });
    },
  }
}
</script>

<style scoped>
.container-participant:hover {
  .icon {
    visibility: visible;
  }
}

.container-participant {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 8px;
}

.icon {
  visibility: hidden;
  display: flex;
  cursor: pointer;
  width: 24px;
  height: 24px;
  margin: 4px;
  color: white;
}

</style>
