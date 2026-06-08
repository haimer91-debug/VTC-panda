import { useState, useEffect, useCallback, useRef } from 'react';
import {
  StyleSheet, Text, View, TextInput, TouchableOpacity,
  FlatList, ActivityIndicator, I18nManager,
  ScrollView, KeyboardAvoidingView, Platform, Modal,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import * as DocumentPicker from 'expo-document-picker';
import { API_URL } from './config';
import { t, LANGS } from './i18n';

I18nManager.allowRTL(true);

// ── Tiny API helper ───────────────────────────────────────────────────────────
async function api(path, opts = {}) {
  const r = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...opts,
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

async function uploadFile(userId, file) {
  const form = new FormData();
  form.append('file', { uri: file.uri, name: file.name, type: file.mimeType || 'application/octet-stream' });
  const r = await fetch(`${API_URL}/users/${userId}/import`, { method: 'POST', body: form });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

function AppInner() {
  const [userId, setUserId] = useState(null);
  const [username, setUsername] = useState('');
  const [tab, setTab] = useState('sessions');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [lang, setLang] = useState('he');
  const cycleLang = () => setLang((l) => LANGS[(LANGS.indexOf(l) + 1) % LANGS.length]);

  const login = async () => {
    if (!username.trim()) return;
    setLoading(true); setError('');
    try {
      const data = await api('/auth/login', {
        method: 'POST', body: JSON.stringify({ username: username.trim() }),
      });
      setUserId(data.user_id);
    } catch {
      setError(t(lang, 'loginError'));
    } finally { setLoading(false); }
  };

  const logout = () => { setUserId(null); setUsername(''); setTab('sessions'); };

  if (!userId) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" />
        <TouchableOpacity onPress={cycleLang} style={styles.langBtn}>
          <Text style={styles.langBtnText}>{lang.toUpperCase()}</Text>
        </TouchableOpacity>
        <Text style={styles.logo}>🎾</Text>
        <Text style={styles.title}>{t(lang, 'appName')}</Text>
        <Text style={styles.subtitle}>{t(lang, 'loginPrompt')}</Text>
        <TextInput
          style={styles.input} placeholder={t(lang, 'username')} placeholderTextColor="#888"
          value={username} onChangeText={setUsername} autoCapitalize="none"
        />
        <TouchableOpacity style={styles.button} onPress={login} disabled={loading}>
          {loading ? <ActivityIndicator color="#111" /> : <Text style={styles.buttonText}>{t(lang, 'login')}</Text>}
        </TouchableOpacity>
        {!!error && <Text style={styles.error}>{error}</Text>}
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />
      <View style={styles.topBar}>
        <TouchableOpacity onPress={logout}><Text style={styles.logout}>{t(lang, 'logout')}</Text></TouchableOpacity>
        <Text style={styles.topTitle}>🎾 {userId}</Text>
        <TouchableOpacity onPress={cycleLang} style={styles.langBtnSmall}>
          <Text style={styles.langBtnText}>{lang.toUpperCase()}</Text>
        </TouchableOpacity>
      </View>

      <View style={{ flex: 1 }}>
        {tab === 'sessions' && <SessionsScreen userId={userId} lang={lang} />}
        {tab === 'chat'     && <ChatScreen userId={userId} lang={lang} />}
        {tab === 'profile'  && <ProfileScreen userId={userId} lang={lang} />}
      </View>

      <View style={styles.tabBar}>
        <TabBtn active={tab === 'profile'}  label={t(lang, 'tabProfile')}  icon="⚙️" onPress={() => setTab('profile')} />
        <TabBtn active={tab === 'chat'}     label={t(lang, 'tabChat')}     icon="💬" onPress={() => setTab('chat')} />
        <TabBtn active={tab === 'sessions'} label={t(lang, 'tabSessions')} icon="🎬" onPress={() => setTab('sessions')} />
      </View>
    </SafeAreaView>
  );
}

export default function App() {
  return (
    <SafeAreaProvider>
      <AppInner />
    </SafeAreaProvider>
  );
}

function TabBtn({ active, label, icon, onPress }) {
  return (
    <TouchableOpacity style={styles.tabBtn} onPress={onPress}>
      <Text style={{ fontSize: 22 }}>{icon}</Text>
      <Text style={[styles.tabLabel, active && styles.tabLabelActive]}>{label}</Text>
    </TouchableOpacity>
  );
}

// ── Sessions ──────────────────────────────────────────────────────────────────
function SessionsScreen({ userId, lang }) {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selected, setSelected] = useState(null);

  const load = useCallback(async () => {
    setLoading(true); setError('');
    try { setSessions(await api(`/users/${userId}/sessions?limit=30`)); }
    catch { setError(t(lang, 'sessionsError')); }
    finally { setLoading(false); }
  }, [userId, lang]);

  useEffect(() => { load(); }, [load]);

  return (
    <View style={{ flex: 1 }}>
      <Text style={styles.screenTitle}>{t(lang, 'sessionsTitle')}</Text>
      {!!error && <Text style={styles.error}>{error}</Text>}
      <FlatList
        data={sessions}
        keyExtractor={(it) => it.match_id}
        contentContainerStyle={{ paddingBottom: 16 }}
        onRefresh={load}
        refreshing={loading}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.card} onPress={() => setSelected(item)}>
            <Text style={styles.cardDate}>{item.date}</Text>
            <Text style={styles.cardStats}>{item.shots} {t(lang, 'shots')} · {item.stats?.in_pct ?? '—'}% IN</Text>
            {!!item.note?.opponent && <Text style={styles.cardOpp}>{t(lang, 'opponent')}: {item.note.opponent}</Text>}
          </TouchableOpacity>
        )}
        ListEmptyComponent={!loading && <Text style={styles.empty}>{t(lang, 'sessionsEmpty')}</Text>}
      />
      <Modal visible={!!selected} animationType="slide" transparent onRequestClose={() => setSelected(null)}>
        <View style={styles.modalBackdrop}>
          <View style={styles.modalSheet}>
            <Text style={styles.screenTitle}>{selected?.date}</Text>
            <ScrollView style={{ maxHeight: 360 }}>
              <Text style={styles.cardStats}>{t(lang, 'shots')}: {selected?.shots ?? '—'}</Text>
              <Text style={styles.cardStats}>{t(lang, 'rallies')}: {selected?.rallies ?? '—'}</Text>
              {selected?.stats?.in_pct != null && (
                <Text style={styles.cardStats}>IN: {selected.stats.in_pct}%</Text>
              )}
              {selected?.stats?.strokes && Object.entries(selected.stats.strokes).map(([name, st]) => (
                <Text key={name} style={styles.cardOpp}>
                  {name}: {st.count} · {t(lang, 'shots')} · {st.avg_speed}km/h ({st.in_pct}% IN)
                </Text>
              ))}
              {!!selected?.note?.opponent && <Text style={styles.cardOpp}>{t(lang, 'opponent')}: {selected.note.opponent}</Text>}
              {!!selected?.note?.score && <Text style={styles.cardOpp}>{t(lang, 'score')}: {selected.note.score}</Text>}
            </ScrollView>
            <TouchableOpacity style={styles.button} onPress={() => setSelected(null)}>
              <Text style={styles.buttonText}>{t(lang, 'close')}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

// ── Chat ──────────────────────────────────────────────────────────────────────
function ChatScreen({ userId, lang }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [convos, setConvos] = useState([]);
  const [savedMsg, setSavedMsg] = useState('');
  const [convoId, setConvoId] = useState(null);
  const scrollRef = useRef(null);

  const scrollEnd = () => setTimeout(() => scrollRef.current?.scrollToEnd({ animated: true }), 80);

  const send = async () => {
    const text = input.trim();
    if (!text || sending) return;
    const next = [...messages, { role: 'user', content: text }];
    setMessages(next);
    setInput('');
    setSending(true);
    scrollEnd();
    try {
      const r = await api(`/users/${userId}/chat`, {
        method: 'POST', body: JSON.stringify({ messages: next }),
      });
      setMessages([...next, { role: 'assistant', content: r.reply }]);
    } catch {
      setMessages([...next, { role: 'assistant', content: t(lang, 'chatError') }]);
    } finally { setSending(false); scrollEnd(); }
  };

  const saveChat = async () => {
    if (!messages.length) return;
    try {
      if (convoId) {
        await api(`/users/${userId}/conversations/${convoId}`, {
          method: 'PUT', body: JSON.stringify({ messages }),
        });
      } else {
        const r = await api(`/users/${userId}/conversations`, {
          method: 'POST', body: JSON.stringify({ messages }),
        });
        if (r.id) setConvoId(r.id);
      }
      setSavedMsg(t(lang, 'chatSaved'));
      setTimeout(() => setSavedMsg(''), 2000);
    } catch {
      setSavedMsg(t(lang, 'chatError'));
      setTimeout(() => setSavedMsg(''), 2000);
    }
  };

  const newChat = () => { setMessages([]); setConvoId(null); };

  const openHistory = async () => {
    setShowHistory(true);
    try { setConvos(await api(`/users/${userId}/conversations`)); } catch { setConvos([]); }
  };

  const openConvo = async (id) => {
    try {
      const c = await api(`/users/${userId}/conversations/${id}`);
      setMessages(c.messages || []);
      setConvoId(id);
      setShowHistory(false);
      scrollEnd();
    } catch {}
  };

  return (
    <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : 'height'} keyboardVerticalOffset={90}>
      <Text style={styles.screenTitle}>{t(lang, 'chatTitle')}</Text>
      <View style={styles.chatTopRow}>
        <TouchableOpacity onPress={openHistory}><Text style={styles.linkAction}>{t(lang, 'chatHistory')}</Text></TouchableOpacity>
        <TouchableOpacity onPress={saveChat} disabled={!messages.length}>
          <Text style={[styles.linkAction, !messages.length && { opacity: 0.4 }]}>{t(lang, 'chatSave')}</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={newChat}><Text style={styles.linkAction}>{t(lang, 'chatNew')}</Text></TouchableOpacity>
      </View>
      {!!savedMsg && <Text style={[styles.cardOpp, { textAlign: 'center' }]}>{savedMsg}</Text>}
      <ScrollView ref={scrollRef} style={{ flex: 1 }} contentContainerStyle={{ paddingBottom: 12 }}>
        {messages.length === 0 && <Text style={styles.empty}>{t(lang, 'chatEmpty')}</Text>}
        {messages.map((m, i) => (
          <View key={i} style={[styles.bubble, m.role === 'user' ? styles.bubbleUser : styles.bubbleBot]}>
            <Text style={[styles.bubbleText, m.role === 'user' ? styles.bubbleTextUser : styles.bubbleTextBot]}>{m.content}</Text>
          </View>
        ))}
        {sending && <ActivityIndicator color="#BBFD00" style={{ marginTop: 8 }} />}
      </ScrollView>
      <View style={styles.chatInputRow}>
        <TouchableOpacity style={styles.sendBtn} onPress={send} disabled={sending}>
          <Text style={styles.sendBtnText}>{t(lang, 'send')}</Text>
        </TouchableOpacity>
        <TextInput
          style={styles.chatInput} placeholder={t(lang, 'chatPlaceholder')} placeholderTextColor="#888"
          value={input} onChangeText={setInput} multiline
          onFocus={scrollEnd}
        />
      </View>

      <Modal visible={showHistory} animationType="slide" transparent onRequestClose={() => setShowHistory(false)}>
        <View style={styles.modalBackdrop}>
          <View style={styles.modalSheet}>
            <Text style={styles.screenTitle}>{t(lang, 'chatHistory')}</Text>
            <ScrollView style={{ maxHeight: 360 }}>
              {convos.length === 0 && <Text style={styles.empty}>{t(lang, 'chatHistoryEmpty')}</Text>}
              {convos.map((c) => (
                <TouchableOpacity key={c.id} style={styles.card} onPress={() => openConvo(c.id)}>
                  <Text style={styles.cardDate}>{c.title}</Text>
                  <Text style={styles.cardOpp}>{c.date}</Text>
                </TouchableOpacity>
              ))}
            </ScrollView>
            <TouchableOpacity style={styles.button} onPress={() => setShowHistory(false)}>
              <Text style={styles.buttonText}>{t(lang, 'close')}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </KeyboardAvoidingView>
  );
}

// ── Profile ───────────────────────────────────────────────────────────────────
function ProfileScreen({ userId, lang }) {
  const [profile, setProfile] = useState(null);
  const [saving, setSaving] = useState(false);

  const load = useCallback(() => {
    api(`/users/${userId}/profile`).then(setProfile).catch(() => {});
  }, [userId]);
  useEffect(() => { load(); }, [load]);

  const setSport = async (sport) => {
    if (saving || profile?.sport === sport) return;
    setSaving(true);
    setProfile((p) => ({ ...p, sport }));
    try {
      await api(`/users/${userId}/profile`, { method: 'PATCH', body: JSON.stringify({ sport }) });
    } catch {} finally { setSaving(false); }
  };

  return (
    <View style={{ flex: 1 }}>
      <Text style={styles.screenTitle}>{t(lang, 'profileTitle')}</Text>
      <View style={styles.card}>
        <Text style={styles.cardDate}>{t(lang, 'name')}: {profile?.username || userId}</Text>
        <Text style={styles.cardStats}>{t(lang, 'ntrpCurrent')}: {profile?.ntrp || '—'}</Text>
        <Text style={styles.cardStats}>{t(lang, 'ntrpNext')}: {profile?.ntrp_next || '—'}</Text>
      </View>

      <Text style={[styles.cardOpp, { marginTop: 18, textAlign: 'right' }]}>{t(lang, 'sport')}</Text>
      <View style={styles.sportRow}>
        <TouchableOpacity
          style={[styles.sportBtn, profile?.sport === 'padel' && styles.sportBtnActive]}
          onPress={() => setSport('padel')}>
          <Text style={[styles.sportBtnText, profile?.sport === 'padel' && styles.sportBtnTextActive]}>{t(lang, 'padel')} 🎾</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.sportBtn, profile?.sport === 'tennis' && styles.sportBtnActive]}
          onPress={() => setSport('tennis')}>
          <Text style={[styles.sportBtnText, profile?.sport === 'tennis' && styles.sportBtnTextActive]}>{t(lang, 'tennis')} 🎾</Text>
        </TouchableOpacity>
      </View>

      <ImportBox userId={userId} lang={lang} onImported={load} />
    </View>
  );
}

function ImportBox({ userId, lang, onImported }) {
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState('');
  const [link, setLink] = useState('');

  const showResult = (r) => {
    const imported = r.imported ?? 0;
    const dup = r.skipped ?? r.duplicates ?? 0;
    setMsg(`${t(lang, 'importOk')}: ${imported}${dup ? ` (${dup} ${t(lang, 'importDup')})` : ''}`);
    onImported && onImported();
  };

  const pick = async () => {
    if (busy) return;
    setMsg('');
    const res = await DocumentPicker.getDocumentAsync({ multiple: false, copyToCacheDirectory: true });
    if (res.canceled || !res.assets?.length) return;
    const file = res.assets[0];
    setBusy(true);
    setMsg(t(lang, 'importing'));
    try {
      showResult(await uploadFile(userId, file));
    } catch {
      setMsg(t(lang, 'importErr'));
    } finally { setBusy(false); }
  };

  const importFromLink = async () => {
    const url = link.trim();
    if (!url || busy) return;
    setBusy(true);
    setMsg(t(lang, 'importing'));
    try {
      const r = await api(`/users/${userId}/import_link`, { method: 'POST', body: JSON.stringify({ url }) });
      setLink('');
      showResult(r);
    } catch {
      setMsg(t(lang, 'importLinkBad'));
    } finally { setBusy(false); }
  };

  return (
    <View style={{ marginTop: 18 }}>
      <Text style={[styles.cardOpp, { textAlign: 'right' }]}>{t(lang, 'importTitle')}</Text>

      <View style={styles.linkRow}>
        <TouchableOpacity style={styles.sendBtn} onPress={importFromLink} disabled={busy || !link.trim()}>
          <Text style={styles.sendBtnText}>{t(lang, 'importLinkBtn')}</Text>
        </TouchableOpacity>
        <TextInput
          style={styles.chatInput} placeholder={t(lang, 'importLinkPlaceholder')} placeholderTextColor="#888"
          value={link} onChangeText={setLink} autoCapitalize="none"
        />
      </View>

      <Text style={[styles.empty, { marginTop: 6, marginBottom: 2 }]}>{t(lang, 'importOr')}</Text>

      <TouchableOpacity style={styles.button} onPress={pick} disabled={busy}>
        {busy ? <ActivityIndicator color="#111" /> : <Text style={styles.buttonText}>{t(lang, 'importPick')}</Text>}
      </TouchableOpacity>
      {!!msg && <Text style={styles.cardOpp}>{msg}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#111', paddingHorizontal: 16, paddingTop: 50 },
  logo: { fontSize: 56, textAlign: 'center', marginBottom: 8 },
  title: { fontSize: 22, fontWeight: '900', color: '#fff', textAlign: 'center', marginBottom: 4 },
  subtitle: { fontSize: 14, color: '#aaa', textAlign: 'center', marginBottom: 24 },
  screenTitle: { fontSize: 18, fontWeight: '900', color: '#fff', textAlign: 'right', marginBottom: 10 },
  input: { backgroundColor: '#1e1e1e', color: '#fff', borderRadius: 10, padding: 14, marginBottom: 14, textAlign: 'right', fontSize: 16 },
  button: { backgroundColor: '#BBFD00', borderRadius: 10, padding: 14, alignItems: 'center' },
  buttonText: { color: '#111', fontWeight: '900', fontSize: 16 },
  error: { color: '#ff6b6b', textAlign: 'center', marginTop: 12 },
  card: { backgroundColor: '#1e1e1e', borderRadius: 12, padding: 16, marginTop: 10 },
  cardDate: { color: '#BBFD00', fontWeight: '700', fontSize: 15, textAlign: 'right' },
  cardStats: { color: '#fff', marginTop: 6, textAlign: 'right' },
  cardOpp: { color: '#aaa', marginTop: 4, textAlign: 'right' },
  empty: { color: '#888', textAlign: 'center', marginTop: 30 },
  topBar: { flexDirection: 'row-reverse', justifyContent: 'space-between', alignItems: 'center', paddingBottom: 10 },
  topTitle: { color: '#fff', fontWeight: '900', fontSize: 17 },
  logout: { color: '#ff6b6b', fontSize: 14 },
  tabBar: { flexDirection: 'row-reverse', borderTopWidth: 1, borderTopColor: '#222', paddingTop: 8, paddingBottom: 6 },
  tabBtn: { flex: 1, alignItems: 'center' },
  tabLabel: { color: '#888', fontSize: 12, marginTop: 2 },
  tabLabelActive: { color: '#BBFD00', fontWeight: '700' },
  bubble: { borderRadius: 12, padding: 12, marginTop: 8, maxWidth: '85%' },
  bubbleUser: { backgroundColor: '#BBFD00', alignSelf: 'flex-end' },
  bubbleBot: { backgroundColor: '#1e1e1e', alignSelf: 'flex-start' },
  bubbleText: { textAlign: 'right' },
  bubbleTextUser: { color: '#111' },
  bubbleTextBot: { color: '#fff' },
  chatInputRow: { flexDirection: 'row-reverse', alignItems: 'flex-end', paddingTop: 8, gap: 8 },
  chatInput: { flex: 1, backgroundColor: '#1e1e1e', color: '#fff', borderRadius: 10, padding: 12, textAlign: 'right', maxHeight: 100 },
  sendBtn: { backgroundColor: '#BBFD00', borderRadius: 10, paddingVertical: 12, paddingHorizontal: 18 },
  sendBtnText: { color: '#111', fontWeight: '900' },
  sportRow: { flexDirection: 'row-reverse', gap: 10, marginTop: 8 },
  sportBtn: { flex: 1, backgroundColor: '#1e1e1e', borderRadius: 10, paddingVertical: 14, alignItems: 'center', borderWidth: 1, borderColor: '#222' },
  sportBtnActive: { backgroundColor: '#BBFD00', borderColor: '#BBFD00' },
  sportBtnText: { color: '#888', fontWeight: '700' },
  sportBtnTextActive: { color: '#111' },
  modalBackdrop: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'flex-end' },
  modalSheet: { backgroundColor: '#1e1e1e', borderTopLeftRadius: 18, borderTopRightRadius: 18, padding: 18, paddingBottom: 30 },
  langBtn: { position: 'absolute', top: 50, left: 16, backgroundColor: '#1e1e1e', borderRadius: 8, paddingVertical: 6, paddingHorizontal: 12 },
  langBtnSmall: { backgroundColor: '#1e1e1e', borderRadius: 8, paddingVertical: 4, paddingHorizontal: 10 },
  langBtnText: { color: '#BBFD00', fontWeight: '700', fontSize: 12 },
  linkRow: { flexDirection: 'row-reverse', alignItems: 'center', gap: 8, marginTop: 8 },
  chatTopRow: { flexDirection: 'row-reverse', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6, gap: 14 },
  linkAction: { color: '#BBFD00', fontSize: 13, fontWeight: '700' },
});
