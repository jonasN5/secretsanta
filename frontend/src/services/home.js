import axios from "@/axios";
import {Participant} from "@/models/Participant.js";
import {Draw} from "@/models/Draw.js";
import store from "@/store/index.js";


/**
 * Get all participants.
 * @returns {Promise<Participant[]>}
 */
export async function participantsSet() {
    const response = await axios
        .get(`/participants/`)
    const participants = response.data.map(participant => new Participant(participant.id, participant.username, participant.email, participant.blacklisted));
    // We'll also replace the blacklisted ids with the actual participants
    participants.forEach(participant => {
        const blacklistedIds = participant.blacklisted;
        participant.blacklisted = blacklistedIds.map(blacklistedId => participants.find(p => p.id === blacklistedId));
    });
    store.commit('setParticipants', participants);
    return store.state.participants;
}


/**
 * Create a new participant.
 * @param {string} username
 * @param {string} email
 * @param {Participant[]} blacklisted the list of blacklisted participants
 * @returns {Promise<Participant>}
 */
export async function participantCreate(username, email, blacklisted) {
    const response = await axios
        .post(`/participants/`, {
            'username': username,
            'email': email,
            'blacklisted': blacklisted.map(p => p.id),
        })
    const participant = new Participant(
        response.data.id,
        response.data.username,
        response.data.email,
        blacklisted,
    );
    store.commit('addParticipant', participant);
    return participant;
}


/**
 * Update a participant.
 * @param participant
 * @returns {Promise<Participant>}
 */
export async function participantUpdate(participant) {
    const response = await axios
        .patch(`/participants/${participant.id}/`, {
            'username': participant.username,
            'email': participant.email,
            'blacklisted': participant.blacklisted.map(p => p.id),
        })
    store.commit('participantUpdate', participant);
    return participant;
}


/**
 * Delete a participant.
 * @param {number} id the id of the participant to delete
 * @returns {Promise<any>}
 */
export async function participantDelete(id) {
    const response = await axios
        .delete(`/participants/${id}/`)
    store.commit('participantDelete', id);
    return response.data;
}

/**
 * Get the last 5 draws.
 * @returns {Promise<Draw[]>}
 */
export async function drawsGet() {
    const response = await axios
        .get(`/draws/`)
    return response.data.results.map(draw => new Draw(draw.id, draw.owner, draw.pairs, draw.created_at));
}


/**
 * Create a new draw.
 * @returns {Promise<Draw>}
 */
export async function drawCreate() {
    const response = await axios
        .post(`/draws/`)
    return new Draw(response.data.id, response.data.owner, response.data.pairs, response.data.created_at);
}