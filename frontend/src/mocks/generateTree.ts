import { v4 as uuidv4 } from 'uuid';

export interface TreeViewBaseItem {
  id: string;
  parent_id: string | null;
  name: string;
  text: string;
  subscription_type: 'free' | 'premium';
  content: {
    id: string;
    menu_id: string;
    type: number;
    server_path: string;
    created_at: string;
    updated_at: string;
  }[];
  children_names: string[];
  children: TreeViewBaseItem[];
}

function generateNode(
  level: number,
  maxLevel: number,
  childrenCount: number,
): TreeViewBaseItem {
  const id = uuidv4();
  const children: TreeViewBaseItem[] = [];
  const children_names: string[] = [];

  if (level < maxLevel) {
    for (let i = 1; i <= childrenCount; i++) {
      const childNode = generateNode(level + 1, maxLevel, childrenCount);
      children.push(childNode);
      children_names.push(childNode.name);
    }
  }

  return {
    id,
    parent_id: level === 0 ? null : '',
    name: `Узел L${level}-${Math.floor(Math.random() * 1000)}`,
    text: `Текст для узла L${level}`,
    subscription_type: Math.random() > 0.8 ? 'premium' : 'free',
    content: [
      {
        id: uuidv4(),
        menu_id: id,
        type: Math.floor(Math.random() * 3) + 1,
        server_path: `https://example.com/content/${Math.floor(Math.random() * 1000)}.jpg`,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ],
    children_names,
    children,
  };
}

function setParentIds(node: TreeViewBaseItem, parentId: string | null = null) {
  node.parent_id = parentId;
  for (const child of node.children) {
    setParentIds(child, node.id);
  }
}

const rootNode = generateNode(0, 4, 5);
setParentIds(rootNode);

export const MOCK_MENU_TREE: TreeViewBaseItem[] = [
  {
    id: '00000000-0000-0000-0000-000000000001',
    parent_id: null,
    name: 'Главное меню',
    text: 'Здравствуйте! Я бот-помощник "ано я тебя слышу". Мы помогаем семьям с детьми с нарушением слуха. Здесь вы найдете проверенную информацию и поддержку на каждом этапе. Чтобы я мог показать вам самые нужные материалы, выберите, пожалуйста, ваш путь.',
    subscription_type: 'free',
    content: [],
    children_names: ['Я волнуюсь о своем слухе', 'Я волнуюсь о слухе ребенка'],
    children: [
      {
        id: '00000000-0000-0000-0000-000000000003',
        parent_id: '00000000-0000-0000-0000-000000000001',
        name: 'Я волнуюсь о своем слухе',
        text: 'Раздел для взрослых с нарушением слуха находится в разработке.',
        subscription_type: 'free',
        content: [],
        children_names: [],
        children: [],
      },
      {
        id: '00000000-0000-0000-0000-000000000002',
        parent_id: '00000000-0000-0000-0000-000000000001',
        name: 'Я волнуюсь о слухе ребенка',
        text: 'Вы выбрали раздел для родителей. Это большой путь, и вы не одни. Мы собрали информацию по самым важным темам — от первых шагов после диагноза до вопросов школы и социализации. Выберите, что вас беспокоит в первую очередь.',
        subscription_type: 'free',
        content: [],
        children_names: [
          'Диагноз: что делать?',
          'Задать свой вопрос',
          'Инклюзия в детском саду и школе',
          'Обучение, развитие и социализация',
          'Поддержка для родителей',
          'Слуховые аппараты и кохлеарные импланты',
        ],
        children: [
          {
            id: '00000000-0000-0000-0000-000000000011',
            parent_id: '00000000-0000-0000-0000-000000000002',
            name: 'Диагноз: что делать?',
            text: 'Получение диагноза — это время сильных эмоций: растерянность, страх, непонимание. Это абсолютно нормально. Давайте пройдем этот путь шаг за шагом. Что вас волнует прямо сейчас?',
            subscription_type: 'free',
            content: [
              {
                id: '71978a3d-8a68-4a1d-99f8-0e9082501da8',
                menu_id: '00000000-0000-0000-0000-000000000011',
                type: 1,
                server_path: 'https://example.com/images/diagnosis_help.jpg',
                created_at: '2025-09-30T20:33:08.016528',
                updated_at: '2025-09-30T20:33:08.016528',
              },
              {
                id: '228bd3bf-5f8b-4e50-8f73-29dbff6e6949',
                menu_id: '00000000-0000-0000-0000-000000000011',
                type: 2,
                server_path: 'https://example.com/videos/first_steps.mp4',
                created_at: '2025-09-30T20:33:08.016528',
                updated_at: '2025-09-30T20:33:08.016528',
              },
            ],
            children_names: [
              'Как справиться с шоком?',
              'Первые шаги: краткий план',
              'Понимание диагноза',
            ],
            children: [
              {
                id: '00000000-0000-0000-0000-000000000022',
                parent_id: '00000000-0000-0000-0000-000000000011',
                name: 'Как справиться с шоком?',
                text: 'Как принять новость? Что является нормальной реакцией? Поддержка семьи: как разговаривать с партнёром, родственниками. Где найти помощь: группы взаимопомощи, горячие линии, психологи.',
                subscription_type: 'free',
                content: [],
                children_names: [],
                children: [],
              },
              {
                id: '00000000-0000-0000-0000-000000000021',
                parent_id: '00000000-0000-0000-0000-000000000011',
                name: 'Первые шаги: краткий план',
                text: 'Как действовать в первые дни: куда обратиться, какие документы нужны. Ключевые специалисты: сурдолог, ЛОР, аудиолог — кого и в какой последовательности посетить.',
                subscription_type: 'free',
                content: [],
                children_names: [],
                children: [],
              },
              {
                id: '00000000-0000-0000-0000-000000000023',
                parent_id: '00000000-0000-0000-0000-000000000011',
                name: 'Понимание диагноза',
                text: 'Типы нарушений слуха: лёгкая, средняя, тяжёлая, глухота. Почему это важно: как тип и степень влияют на методы коррекции. Может ли слух измениться: динамика состояния, контрольные проверки.',
                subscription_type: 'free',
                content: [],
                children_names: [],
                children: [],
              },
            ],
          },
          {
            id: '00000000-0000-0000-0000-000000000016',
            parent_id: '00000000-0000-0000-0000-000000000002',
            name: 'Задать свой вопрос',
            text: 'Если вы не нашли ответа на свой вопрос в нашей библиотеке, напишите его здесь. Мы обработаем ваш запрос и добавим недостающую информацию.',
            subscription_type: 'free',
            content: [],
            children_names: [],
            children: [],
          },
          {
            id: '00000000-0000-0000-0000-000000000014',
            parent_id: '00000000-0000-0000-0000-000000000002',
            name: 'Инклюзия в детском саду и школе',
            text: 'Успешная инклюзия — это командная работа семьи, педагогов и ребенка. Здесь вы найдете практические руководства по правам, адаптации среды и выстраиванию отношений с образовательным учреждением.',
            subscription_type: 'free',
            content: [],
            children_names: [],
            children: [],
          },
          {
            id: '00000000-0000-0000-0000-000000000013',
            parent_id: '00000000-0000-0000-0000-000000000002',
            name: 'Обучение, развитие и социализация',
            text: 'Развитие ребенка с нарушением слуха имеет свои особенности. Важно правильно выстроить занятия по развитию слуха и речи, а также помочь ребенку общаться со сверстниками.',
            subscription_type: 'free',
            content: [],
            children_names: [],
            children: [],
          },
          {
            id: '00000000-0000-0000-0000-000000000015',
            parent_id: '00000000-0000-0000-0000-000000000002',
            name: 'Поддержка для родителей',
            text: 'Забота о себе — это необходимость. Чтобы быть опорой для ребенка, важно восстанавливать силы. Здесь вы найдете психологическую помощь, общение с теми, кто понимает, и ответы на вопросы.',
            subscription_type: 'free',
            content: [],
            children_names: [],
            children: [],
          },
          {
            id: '00000000-0000-0000-0000-000000000012',
            parent_id: '00000000-0000-0000-0000-000000000002',
            name: 'Слуховые аппараты и кохлеарные импланты',
            text: 'Компенсация слуха — важный шаг, который открывает ребенку мир звуков. Здесь мы поможем разобраться в видах аппаратов, процессе их выбора, получения и привыкания.',
            subscription_type: 'free',
            content: [
              {
                id: '7df147a7-2068-47f7-872f-b74a6c5a6e99',
                menu_id: '00000000-0000-0000-0000-000000000012',
                type: 1,
                server_path: 'https://example.com/images/hearing_aids.jpg',
                created_at: '2025-09-30T20:33:08.016528',
                updated_at: '2025-09-30T20:33:08.016528',
              },
              {
                id: 'e3f8a013-b5c4-461f-8c28-76d42201058c',
                menu_id: '00000000-0000-0000-0000-000000000012',
                type: 3,
                server_path: 'https://example.com/documents/guide.pdf',
                created_at: '2025-09-30T20:33:08.016528',
                updated_at: '2025-09-30T20:33:08.016528',
              },
            ],
            children_names: [],
            children: [],
          },
        ],
      },
    ],
  },
  rootNode,
];
