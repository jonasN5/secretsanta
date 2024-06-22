import {createStore} from 'vuex'


export default createStore({
    state() {
        return {
            participants: []
        }
    },
    mutations: {
        setParticipants(state, participants) {
            state.participants = participants;
        },
        addParticipant(state, participant) {
            state.participants.push(participant);
        },
        participantDelete(state, id) {
            state.participants = state.participants.filter(participant => participant.id !== id);
        },
        participantUpdate(state, participant) {
            const index = state.participants.findIndex(p => p.id === participant.id);
            state.participants[index] = participant;
        }
    },
})