import { FaEnvelope, FaGithub, FaInstagram, FaDiscord } from "react-icons/fa";
import styles from "./Contact.module.css";

function Contact() {
  return (
    <div className={styles.contact_us}>
      <div className={styles.social_links}>
        <a href="mailto:adryellpaulo@gmail.com">
          <FaEnvelope /> E-mail
        </a>
        <a
          href="https://github.com/adryells"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaGithub /> GitHub
        </a>
        <a
          href="https://www.instagram.com/_adryell.md/"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaInstagram /> Instagram
        </a>
        <a
          href="<SEU_LINK_DO_DISCORD>"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaDiscord /> Discord
        </a>
      </div>
    </div>
  );
}

export default Contact;
