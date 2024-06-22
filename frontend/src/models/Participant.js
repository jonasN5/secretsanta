export class Participant {
  constructor(id, username, email, blacklisted) {
    this.id = id;
    this.username = username;
    this.email = email;
    this.blacklisted = blacklisted;
  }

  get label() {
    return this.username ? this.username : this.email;
  }
}